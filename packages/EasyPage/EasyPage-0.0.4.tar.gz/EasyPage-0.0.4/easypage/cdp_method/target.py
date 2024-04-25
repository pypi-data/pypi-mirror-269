from typing import Tuple
from easypage.conn import Conn


class Target:
    """
        Target

        https://chromedevtools.github.io/devtools-protocol/tot/Target
    """

    def set_discover_targets(
            self,
            discover: bool = True,
            raise_err: bool = False,
            need_callback: bool = False,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        控制是否发现可用目标并通过 targetCreated/targetInfoChanged/targetDestroyed 事件进行通知

        https://chromedevtools.github.io/devtools-protocol/tot/Target/#method-setDiscoverTargets

        :param discover: 是否发现可用目标
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        send_data = {
            "discover": discover
        }

        send_data.update(kwargs)

        return self.__conn.send(
            method="Target.setDiscoverTargets",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def __init__(self, conn: Conn):
        self.__conn = conn

    def get_targets(
            self,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        获取所有的 target

        https://chromedevtools.github.io/devtools-protocol/tot/Target/#method-getTargets

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Target.getTargets",
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def get_browser_contexts(
            self,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        获取所有的浏览器上下文

        https://chromedevtools.github.io/devtools-protocol/tot/Target/#method-getBrowserContexts

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Target.getBrowserContexts",
            params=kwargs,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def create_browser_context(
            self,
            proxy: str = None,
            proxy_pass_list: list = None,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        新建上下文

        学习链接：https://chromedevtools.github.io/devtools-protocol/tot/Target/#method-createBrowserContext

        :param proxy: 代理 如：http://127.0.0.1:7890
        :param proxy_pass_list: 代理绕过列表，类似于传递给 --proxy-bypass-list 的列表（表示某些地址不走代理）如：["www.baidu.com"]
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :param kwargs:
        :return:
        """
        if proxy and not proxy.startswith("http"):
            proxy = "http://" + proxy

        send_data = {
            "disposeOnDetach": True,
            "proxyServer": proxy or "",
            "proxyBypassList": ",".join(proxy_pass_list) if proxy_pass_list else ""
        }

        send_data.update(kwargs)

        return self.__conn.send(
            method='Target.createBrowserContext',
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def create_target(
            self,
            url: str = None,
            browser_context_id: str = None,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        创建新的页面

        https://chromedevtools.github.io/devtools-protocol/tot/Target/#method-createTarget

        :param url:
        :param browser_context_id:
        :param kwargs:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        send_data = {
            "url": url or "about:blank",
        }

        if browser_context_id:
            send_data["browserContextId"] = browser_context_id

        send_data.update(kwargs)

        return self.__conn.send(
            method='Target.createTarget',
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def close_target(
            self,
            target_id: str,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        关闭 target

        https://chromedevtools.github.io/devtools-protocol/tot/Target/#method-closeTarget

        :param target_id:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Target.closeTarget",
            params={
                "targetId": target_id
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )
