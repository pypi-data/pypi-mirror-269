"""
    页面 driver
"""
import time
import base64
import websocket
from pathlib import Path
from parsel import Selector
from bs4 import BeautifulSoup
from easypage.logger import logger
from typing import Tuple, Union, List
from easypage.driver.driver import Driver
from easypage.options import BrowserOptions
from easypage import definition, errors, operate
from easypage.conn import TYPE_PAGE, DRIVER_TYPE
from easypage.utils import other_utils, browser_utils


class PageDriver(Driver):
    def __init__(self, opts: BrowserOptions, driver_id: str, context_id: str = None, proxy: definition.Proxy = None):
        """

        :param opts:
        :param driver_id:
        """
        super().__init__(opts, TYPE_PAGE, driver_id)
        self._driver_id = driver_id
        self._context_id = context_id
        self._proxy = proxy
        self._opts = opts

        # 预设参数
        self.__loading = False
        self.__requests_cache = {}

        # 启用事件
        self.cdp.dom.enable()
        self.cdp.page.enable()
        self.cdp.security.set_ignore_certificate_errors()
        self.cdp.fetch.enable(handle_auth_requests=True)

        # 事件监听
        self.on(event='Page.loadEventFired', callback=self.__on_page_load_event_fired)
        self.on(event='Page.frameStartedLoading', callback=self.__on_page_frame_started_loading)
        self.on(event='Page.frameStoppedLoading', callback=self.__on_page_frame_stopped_loading)
        self.on(event='Fetch.requestPaused', callback=self.__on_fetch_request_paused)
        self.on(event='Fetch.authRequired', callback=self.__on_fetch_auth_required)

    def get(self, url, **kwargs) -> Tuple[bool, Union[None, str]]:
        """
        访问某个页面

        返回的第一个值是请求命令是否成功
        返回的第二个值是当请求失败的时候发送原因，比如设置的代理访问不通

        :param url:
        :param kwargs:
        :return:
        """
        if "frameId" not in kwargs:
            kwargs["frameId"] = self._driver_id
        status, result = self.cdp.page.navigate(url=url, **kwargs)
        if not status:
            return False, None

        elif "errorText" in result:
            logger.warning("url：{} errorText：{}", url, result["errorText"])
            return False, result["errorText"]

        return True, None

    def query_selector(
            self,
            selector: str,
            node_id: int = None,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementNotFound]:
        """
        选择元素

        :param selector: 选择器
        :param node_id: 节点 id（基于某个节点查找时需要）
        :param raise_err: 是否报错
        :return:
        """
        status, new_node = self.cdp.dom.query_selector(
            selector=selector,
            node_id=node_id,
            raise_err=raise_err,
        )
        if (status and new_node['nodeId'] == 0) or not new_node or not status:
            if raise_err:
                raise errors.ElementNotFound(selector)
            return None

        return Element(node_id=new_node['nodeId'], page=self)

    def query_selector_all(
            self,
            selector: str,
            node_id: int = None,
            raise_err: bool = False
    ) -> Union[List['Element'], None, errors.ElementNotFound]:
        """
        选择元素

        :param selector: 选择器（支持 css、xpath）
        :param node_id: 节点 id（基于某个节点查找时需要）
        :param raise_err: 是否报错
        :return:
        """
        status, new_nodes = self.cdp.dom.query_selector_all(
            selector=selector,
            node_id=node_id,
            raise_err=raise_err,
        )
        if not status or not new_nodes:
            if raise_err:
                raise errors.ElementNotFound(selector)
            return None

        elements = []
        for nn in new_nodes['nodeIds']:
            elements.append(Element(node_id=nn, page=self))
        return elements

    def eval_js(self, js: str, **kwargs) -> Tuple[bool, any]:
        """
        执行 js 脚本

        :param js: 路径或者 js 字符串
        :return: 可能是字符串、数字等
        """
        status, result = self.cdp.runtime.evaluate(js, **kwargs)
        if not status:
            return status, result

        if 'value' in result['result']:
            return True, result['result']['value']
        else:
            return False, result['result']['description']

    def iframes(self) -> List['IframeElement']:
        """
        获取所有的 iframe

        :return:
        """
        # operate.pages(self._opts.address)

        elements = []

        status, new_node_ids = self.cdp.dom.query_selector_all(
            selector="iframe",
        )
        if not new_node_ids or not status:
            return elements

        for node_id in new_node_ids['nodeIds']:
            status, frame_id = self.cdp.dom.describe_node(nodeId=node_id)
            if not frame_id or not status:
                continue

            frame_id = frame_id['node']['frameId']

            try:
                # TODO 需要思考需不需要加入 BrowserDriver，如何管理
                elements.append(IframeElement(
                    opts=self._opts,
                    driver_id=frame_id,
                    context_id=self._context_id,
                    proxy=self._proxy
                ))
            except websocket.WebSocketBadStatusException:
                logger.warning("当前 iframe 可能已不在页面上：{}", frame_id)

        return elements

    def cookies(self, only_key_val: bool = True, domain: str = None) -> Union[List[dict], dict]:
        """
        获取 cookie

        :param only_key_val: 是否仅返回 {name:'',value:''} 形式
        :param domain: 指定域名
        :return: [{'name': '', 'value': '', 'domain': '', 'path': '', 'expires': -1, 'size': 161, 'httpOnly': True, 'secure': True, 'session': True, 'sameSite': 'Strict', 'priority': 'Medium', 'sameParty': False, 'sourceScheme': 'Secure', 'sourcePort': 443}]
        """
        status, cookies = self.cdp.storage.get_cookies(context_id=self._context_id)
        if not status:
            return []

        cookies = cookies['cookies']

        if only_key_val:
            cookie_dict = {}
            for c in cookies:
                if domain:
                    if c['domain'] == domain:
                        cookie_dict[c['name']] = c['value']
                else:
                    cookie_dict[c['name']] = c['value']

            return cookie_dict
        else:
            if domain:
                return list(filter(lambda x: x['domain'] == domain, cookies))
            return cookies

    def screenshot(
            self,
            save_path: str = None,
            format_type: str = "png",
            quality: int = None,
            clip: dict = None,
            from_surface: bool = True,
            capture_beyond_viewport: bool = False,
            optimize_for_speed: bool = False,
    ) -> bytes:
        """
        截图

        https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-captureScreenshot

        clip 参考：https://chromedevtools.github.io/devtools-protocol/tot/Page/#type-Viewport

        :param save_path: 保存本地的路径
        :param format_type: jpeg, png, webp，默认值为 png
        :param quality: 压缩质量范围为 [0..100]（仅限 jpeg）
        :param clip: 仅捕获给定区域的屏幕截图（{x:1,y:1,width:1,height:1,scale:1}）
        :param from_surface: 从表面捕获屏幕截图，而不是从视图捕获屏幕截图，默认值为 true
        :param capture_beyond_viewport: 捕获视口之外的屏幕截图，默认值为 false
        :param optimize_for_speed: 优化图像编码以提高速度，而不是优化结果大小（默认为 false）
        :return: {"data":""}
        """
        # 等待页面加载
        self.wait_loaded()

        # 截图
        status, data = self.cdp.page.capture_screenshot(
            format_type=format_type,
            quality=quality,
            clip=clip,
            from_surface=from_surface,
            capture_beyond_viewport=capture_beyond_viewport,
            optimize_for_speed=optimize_for_speed
        )

        if not status or not data:
            return b""

        data_bytes = base64.b64decode(data["data"])

        # 保存本地
        if save_path:
            save_path = Path(save_path).absolute().resolve()
            save_path.parent.mkdir(parents=True, exist_ok=True)
            if not save_path.suffix:
                save_path = save_path.with_suffix(".png")

            with open(save_path, "wb") as f:
                f.write(data_bytes)

        return data_bytes

    def close(self):
        """
        关闭当前页面

        :return:
        """
        self.cdp.page.close()

    """
        等待
    """

    def wait_loaded(self, timeout: int = None):
        """
        等待页面加载完成

        :param timeout:
        :return:
        """
        timeout = timeout or self._opts.timeout

        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.__loading:
                return
            time.sleep(0.1)

    def wait_for_selector(
            self,
            selector: str,
            timeout: int = None,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementWaitTimeout]:
        """
        等待某个元素

        :param timeout:
        :param selector:
        :param raise_err:
        :return:
        """
        timeout = timeout or self._opts.timeout

        start_time = time.time()

        while time.time() - start_time < timeout:
            ele = self.query_selector(selector=selector)
            if ele:
                return ele
            time.sleep(0.1)

        if raise_err:
            raise errors.ElementWaitTimeout(selector)

    def wait_for_selectors(
            self,
            selectors: List[str],
            timeout: int = None,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementWaitTimeout]:
        """
        等待多个元素，谁先拿到就返回谁（所以要自己注意放入的顺序）

        :param timeout:
        :param selectors: 元素列表
        :param raise_err:
        :return:
        """
        timeout = timeout or self._opts.timeout

        start_time = time.time()

        while time.time() - start_time < timeout:
            for s in selectors:
                ele = self.query_selector(selector=s)
                if ele:
                    return ele

                if time.time() - start_time >= timeout:
                    break

            time.sleep(0.1)

        if raise_err:
            raise errors.ElementWaitTimeout(selectors)

    """
        访问属性
    """

    @property
    def url(self) -> str:
        """
        当前页面的 url

        :return:
        """
        status, root = self.cdp.dom.get_document()

        if not status:
            return ""

        return root['root']['documentURL']

    @property
    def content(self) -> str:
        """
        当前页面的内容

        :return:
        """
        status, root = self.cdp.dom.get_document()
        if not status:
            return ""

        back_end_node_id = root['root']['backendNodeId']

        status, html = self.cdp.dom.get_outer_html(backendNodeId=back_end_node_id)
        if not status:
            return ""

        return html["outerHTML"]

    """
       事件监听
    """

    @other_utils.catch_error
    def __on_page_load_event_fired(self, *args, **kwargs):
        """
        页面加载完成将会被触发

        :return:
        """
        self.__loading = False
        logger.debug("页面加载耗时：{}", kwargs['timestamp'])

    @other_utils.catch_error
    def __on_page_frame_started_loading(self, *args, **kwargs):
        """
        加载开始

        :return:
        """
        self.__loading = True

    @other_utils.catch_error
    def __on_page_frame_stopped_loading(self, *args, **kwargs):
        """
        加载结束

        :return:
        """
        self.__loading = False

    @other_utils.catch_error
    def __on_fetch_request_paused(self, *args, **kwargs):
        """
        请求监听

        请求将暂停，直到客户端响应 替换为 continueRequest、failRequest 或 fulfillRequest

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#event-requestPaused

        :param args:
        :param kwargs: {"method":"Fetch.requestPaused","params":{"requestId":"interception-job-1.0","request":{"url":"https://www.baidu.com/","method":"GET","headers":{"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36","sec-ch-ua":"\"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"","sec-ch-ua-mobile":"?0","sec-ch-ua-platform":"\"Windows\""},"initialPriority":"VeryHigh","referrerPolicy":"strict-origin-when-cross-origin"},"frameId":"E361A685E14EAEC054BEF17592DF25DF","resourceType":"Document"}}
        :return:
        """
        request_id = kwargs['requestId']
        self.__requests_cache[request_id] = kwargs['request']

        self.cdp.fetch.continue_request(
            request_id=request_id,
        )

    @other_utils.catch_error
    def __on_fetch_auth_required(self, *args, **kwargs):
        """
        监听 authRequired

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#event-authRequired

        :param args:
        :param kwargs:
        :return:
        """
        request_id = kwargs['requestId']

        user = None
        pwd = None
        if self._proxy:
            user = self._proxy.get("user")
            pwd = self._proxy.get("pwd")
        elif self._opts.proxy and "user" in self._opts.proxy and "pwd" in self._opts.proxy:
            user = self._opts.proxy.get("user")
            pwd = self._opts.proxy.get("pwd")

        if not user or not pwd:
            logger.error("未获取到代理的账号密码！")
            return

        self.cdp.fetch.continue_with_auth(
            request_id=request_id,
            user=user,
            pwd=pwd,
        )


"""
    动作链
"""


# modifiers
class Key:
    Alt = 1
    Ctrl = 2
    Backspace = 8
    Shift = 4
    Meta = 8


# windowsVirtualKeyCode
class KeyCode:
    Backspace = 8
    Tab = 9
    Enter = 13
    Shift = 16
    Ctrl = 17
    Alt = 18
    PauseOrBreak = 19
    CapsLock = 20
    Esc = 27
    Space = 32
    PageUp = 33
    PageDown = 34
    End = 35
    Home = 36
    LeftArrow = 37
    UpArrow = 38
    RightArrow = 39
    DownArrow = 40
    Insert = 45
    Delete = 46
    A = 65
    B = 66
    C = 67
    D = 68
    E = 69
    F = 70
    G = 71
    H = 72
    I = 73
    J = 74
    K = 75
    L = 76
    M = 77
    N = 78
    O = 79
    P = 80
    Q = 81
    R = 82
    S = 83
    T = 84
    U = 85
    V = 86
    W = 87
    X = 88
    Y = 89
    Z = 90
    Windows = 91  # Windows 键
    RightClick = 93
    Numpad_0 = 96
    Numpad_1 = 97
    Numpad_2 = 98
    Numpad_3 = 99
    Numpad_4 = 100
    Numpad_5 = 101
    Numpad_6 = 102
    Numpad_7 = 103
    Numpad_8 = 104
    Numpad_9 = 105
    Multiply = 106
    Add = 107
    Subtract = 109
    DecimalPoint = 110
    Divide = 111
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    NumLock = 144
    ScrollLock = 145
    SemiColon = 186
    EqualSign = 187
    Comma = 188
    Dash = 189
    Period = 190
    ForwardSlash = 191
    GraveAccent = 192
    OpenBracket = 219
    BackSlash = 220
    CloseBracket = 221
    SingleQuote = 222


class ActionChain:
    def __init__(self, node_id: int, page: PageDriver):
        self.page = page
        self.node_id = node_id

    def focus(self):
        """
        聚焦

        :return:
        """
        self.page.cdp.dom.focus(nodeId=self.node_id)

    def clear(self, simulation: bool = True):
        """
        清空输入框的值

        :param simulation: 模拟真实操作
        :return:
        """
        if not simulation:
            # 非模拟的话，实际的修改可能并不会生效（元素修改了，但是页面没更改）
            self.page.cdp.dom.set_attribute_value(
                name="value",
                value="",
                node_id=self.node_id,
            )
        else:
            # 全选
            self.ctrl(key=KeyCode.A)

            # 删除
            self.page.cdp.input.dispatch_key_event(
                event_type="rawKeyDown",
                windowsVirtualKeyCode=KeyCode.Backspace,
                modifiers=Key.Backspace,
            )

        return self

    def input_text(self, val: str, simulation: bool = True):
        """
        输入文本（模拟输入）

        :param val:
        :param simulation: 模拟真实操作
        :return:
        """
        if not simulation:
            # 非模拟的话，实际的修改可能并不会生效（元素修改了，但是页面没更改）
            self.page.cdp.dom.set_attribute_value(
                name="value",
                value=val,
                node_id=self.node_id,
            )
        else:
            # 对焦
            self.focus()

            # 输入
            for v in val:
                self.page.cdp.input.dispatch_key_event(
                    event_type="keyDown",
                    is_key_pad=True,
                    key=v,
                    text=v,
                    code="Key " + v.upper(),
                )

                self.page.cdp.input.dispatch_key_event(
                    event_type="keyUp",
                    is_key_pad=True,
                    key=v,
                    text=v,
                    code="Key " + v.upper(),
                )

        return self

    def ctrl(self, key: int):
        """
        ctrl 事件

        :param key: 如 ctrl+A 只要输入 a 或 A 就行了
        :return:
        """
        # 对焦
        self.focus()

        # 输入
        self.page.cdp.input.dispatch_key_event(
            event_type="rawKeyDown",
            windowsVirtualKeyCode=key,
            modifiers=Key.Ctrl,
        )

        return self

    def click(self, count: int = 1, button: str = "middle", simulation: bool = True):
        """
        执行点击

        :param count: 点击次数
        :param button: 点击位置，如：none, left, middle, right, back, forward
        :param simulation: 模拟真实操作
        :return:
        """


"""
    元素
"""


class Element(ActionChain):
    def __init__(self, node_id: int, page: PageDriver):
        """
        生成节点

        :param node_id 当前节点的 id
        :param page PageDriver 对象
        :return:
        """
        super().__init__(node_id, page)

        self.__tagName: str = None

    def query_selector(
            self,
            selector: str,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementNotFound]:
        """
        选择元素

        通过这种绕一圈的书写方式，就可以有编辑器的提示了

        :param selector: 选择器（支持 css、xpath）
        :param raise_err: 是否报错
        :return:
        """
        return self.page.query_selector(
            selector=selector,
            node_id=self.node_id,
            raise_err=raise_err
        )

    def query_selector_all(
            self,
            selector: str,
            raise_err: bool = False
    ) -> Union['Element', None, errors.ElementNotFound]:
        """
        选择元素

        :param selector: 选择器（支持 css、xpath）
        :param raise_err: 是否报错
        :return:
        """
        return self.page.query_selector_all(
            selector=selector,
            raise_err=raise_err,
        )

    def eval_js_on_selector(self, js: str, **kwargs):
        """
        执行 js 脚本（会自动使用 function 包裹，不然无法执行）

        学习链接：https://chromedevtools.github.io/devtools-protocol/tot/Runtime/#method-evaluate

        :param js: 路径或者 js 字符串
        :return:
        """
        js = "function (){ %s }" % js
        return self.page.cdp.runtime.call_function_on(js=js, object_id=self._object_id, **kwargs)

    def click(self, count: int = 1, button: str = "left", raise_err: bool = True, simulation: bool = True):
        """
        执行点击

        :param count: 点击次数
        :param button: 代表鼠标的按键，如：none（不触发按键，代表光标）, left（左击）, middle（滚轮）, right（右击）, back（后退）, forward（前进）
        :param raise_err: 是否抛出错误
        :param simulation: 模拟真实操作
        :return:
        """
        if not simulation:
            self.eval_js_on_selector(js="this.click();", returnByValue=True)
            return
        else:
            # 聚焦
            self.focus()

            # 获取元素坐标
            status, content = self.page.cdp.dom.get_box_model(nodeId=self.node_id, raise_err=raise_err)
            content = content['model']['content']
            x, y = browser_utils.parse_box_center_coordinate(data=content)

            # 移动
            self.page.cdp.input.dispatch_mouse_event(
                event_type="mouseMoved",
                x=x,
                y=y,
                button="none"
            )

            # 点击
            self.page.cdp.input.dispatch_mouse_event(
                event_type="mousePressed",
                x=x,
                y=y,
                button=button,
                clickCount=count
            )

            # 释放
            self.page.cdp.input.dispatch_mouse_event(
                event_type="mouseReleased",
                x=x,
                y=y,
                button=button,
                clickCount=count
            )

        return self

    @property
    def attrs(self) -> dict:
        """
        属性

        :return:
        """
        status, attrs = self.page.cdp.dom.get_attributes(node_id=self.node_id)

        if not status:
            return {}

        return attrs or {}

    @property
    def tag_name(self) -> str:
        """
        节点名称

        :return:
        """
        if not self.__tagName:
            status, describe = self.page.cdp.dom.describe_node(nodeId=self.node_id)
            if status and describe:
                self.__tagName = describe['node']['nodeName'].lower()
        return self.__tagName

    @property
    def html(self) -> str:
        """
        html 文本

        :return: <input type="submit" id="su" value="百度一下" class="bg s_btn">
        """
        status, html = self.page.cdp.dom.get_outer_html(backendNodeId=self._back_end_node_id)

        if not status:
            return ""

        return html["outerHTML"]

    @property
    def text(self):
        """
        获取除了标签以外的内容

        :return:
        """
        return self.soup.get_text()

    @property
    def selector(self) -> Selector:
        """
        获取 parsel 解析器

        :return:
        """
        return Selector(self.html)

    @property
    def soup(self) -> BeautifulSoup:
        """
        获取 bs4 解析器

        :return:
        """
        return BeautifulSoup(self.html, "lxml")

    @property
    def _back_end_node_id(self) -> int:
        """
        获取 backendNodeId

        :return:
        """
        _, node = self.page.cdp.dom.describe_node(nodeId=self.node_id)

        return node['node']['backendNodeId']

    @property
    def _object_id(self) -> str:
        """
        获取 object_id

        :return:
        """
        _, node = self.page.cdp.dom.resolve_node(backendNodeId=self._back_end_node_id)

        return node['object']['objectId']

    def __repr__(self):
        attrs = self.attrs
        attrs_text = ' '.join([f'{i}="{attrs[i]}"' for i in attrs.keys()])
        return f"<{self.__class__.__name__} {self.tag_name} {attrs_text}>"


class IframeElement(PageDriver):
    def __init__(self, opts: BrowserOptions, driver_id: str, context_id: str = None, proxy: definition.Proxy = None):
        super().__init__(opts, driver_id, context_id, proxy)
