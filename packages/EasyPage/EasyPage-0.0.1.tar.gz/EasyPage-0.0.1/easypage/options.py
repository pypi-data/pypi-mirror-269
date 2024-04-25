"""
    启动参数大全：https://peter.sh/experiments/chromium-command-line-switches/
    常用启动参数：https://blog.csdn.net/bigcarp/article/details/121142873

    与浏览器启动无关的可以做 settings 的默认值，否则不可以
"""
import re
import shutil
from pathlib import Path
from typing import List, Union
from easypage import settings, errors, definition


class _OptionsBasicOperations:
    def __init__(self):
        self._args = []
        self._args.extend(settings.BROWSER_START_ARGS)
        self._extensions = set()

    def add(self, args: Union[str, List[str]]) -> None:
        """
        加入启动参数

        :param args:
        :return:
        """
        if isinstance(args, str):
            args = [args]

        for a in args:
            a = a.strip()
            self.remove(a)
            self._args.append(a)

    def remove(self, args: Union[str, List[str]]) -> None:
        """
        移除启动参数（包含关系，只要含有关键词就删除）

        :param args:
        :return:
        """
        if isinstance(args, str):
            args = [args]

        self._args = [a1 for a1 in self._args if not any(a2.strip() in a1 for a2 in args)]

    def exists(self, arg: str) -> Union[str, bool]:
        """
        判断是否存在指定参数（包含关系）

        :param arg:
        :return: 存在返回，不存在返回 False
        """
        arg = arg.strip()

        for a in self._args:
            if arg in a:
                return a
        return False

    @property
    def args(self) -> list:
        """
        获取所有的配置

        :return:
        """
        return self._args

    def clear(self, default: bool = False) -> None:
        """
        清空所有配置

        :param default: 是否清空默认配置
        :return:
        """
        self._args.clear()

        if not default:
            self._args.extend(settings.BROWSER_START_ARGS)

    @property
    def extensions(self) -> set:
        """
        获取所有的插件

        :return:
        """
        return self._extensions


class BrowserOptions(_OptionsBasicOperations):
    def __init__(self):
        super().__init__()
        self._ip: str = None  # type:ignore # 设置浏览器启动ip
        self._port: int = None  # type:ignore # 设置浏览器启动端口
        self._user_data_dir: Path = None  # type:ignore # 设置用户数据目录
        self._delete_user_data_dir_when_stop: bool = True  # 设置用户数据目录是否删除
        self._browser_path: Path = None  # type:ignore # 设置浏览器路径
        self._proxy: definition.Proxy = None  # type:ignore # 设置代理
        self._user_agent: str = None  # type:ignore # 设置 user_agent
        self._headless: bool = False  # 设置浏览器是否隐身
        self._timeout: int = settings.TIMEOUT  # 设置全局超时时间

    """
        程序参数
    """

    def set_address(self, port: int, ip: str = "127.0.0.1"):
        """
        设置浏览器启动端口

        :param ip:
        :param port: 不设置的话，默认是 9876
        :return:
        """
        self._ip = ip.strip().lower().replace('localhost', '127.0.0.1')
        self._port = port

    def set_timeout(self, seconds: int):
        """
        设置全局的超时时间

        :param seconds:
        :return:
        """
        self._timeout = seconds

    def set_extension(self, path: Union[str, Path]):
        """
        添加插件

        :param path: 插件 crx 解压后的路径
        :return:
        """
        path = Path(path).absolute().resolve()

        if not path.exists():
            raise FileNotFoundError(path)

        self._extensions.add(str(path))

    def set_delete_user_data_dir_when_stop(self, enable: bool = True):
        """
        配置是否在结束时删除用户文件夹

        :param enable:
        :return:
        """
        self._delete_user_data_dir_when_stop = enable

    """
        浏览器参数
    """

    def set_user_data_dir(self, path: str, delete_if_exists: bool = False, delete_when_stop: bool = True) -> None:
        """
        设置用户数据目录
        注意：目录代表着配置信息，如果不删除可能配置不会生效！

        :param path:
        :param delete_if_exists: 启动时存在的话是否要删除
        :param delete_when_stop: 程序终止的时候是否删除
        :return:
        """
        path = Path(path).absolute().resolve()
        if delete_if_exists and path.exists():
            shutil.rmtree(path, ignore_errors=True)
        path.mkdir(parents=True, exist_ok=True)

        self.add(f"--user-data-dir={path}")
        self._user_data_dir = path
        self._delete_user_data_dir_when_stop = delete_when_stop

    def set_browser_path(self, path: str):
        """
        配置浏览器路径

        :param path:
        :return:
        """
        path = Path(path).absolute().resolve()

        if not path.exists():
            raise FileNotFoundError(path)
        elif not path.is_file():
            raise TypeError(f"浏览器路径不是文件：{path}")

        self._browser_path = path

    def set_user_agent(self, user_agent: str):
        """
        设置 user_agent

        :param user_agent:
        :return:
        """
        self._user_agent = user_agent.strip()
        self.add(args=f"--user-agent={user_agent.strip()}")

    def set_proxy_server(self, proxy: definition.Proxy):
        """
        设置代理

        这里使用了其它的方式设置含有账号密码的代理，而不是一开始设置
        浏览器启动时不支持 --proxy-server 设置账号密码代理，这一问题是 chromium 自身决定的，而不是开发问题

        :param proxy: 如：http://127.0.0.1:7890
        :return:
        """
        if re.search(r'.*?:.*?@.*?\..*', proxy["server"]):
            raise errors.ProxySetError(msg="""
        代理格式错误，如需要使用账号密码代理，请参照下面的两种方法：
            1、配置默认账号密码
            opts = BrowserOptions()
            opts.set_proxy_server(proxy = {"server": "","user": "","pwd": ""})
            
            2、使用 context 实现：
                browser.new_context(proxy = {"server": "","user": "","pwd": ""})
        """.format(proxy))

        if not proxy["server"].startswith("http"):
            proxy["server"] = "http://" + proxy["server"]

        self.add(args=f'--proxy-server={proxy["server"]}')
        self._proxy = proxy

    def set_window_size(self, width: int, height: int):
        """
        设置窗口大小

        :param width:
        :param height:
        :return:
        """
        self.add(args=f"--window-size={width},{height}")

    """
        涉及启用、禁用的
    """

    def set_headless(self, enable: bool = True):
        """
        设置浏览器是否隐身

        :param enable: 是否启用
        :return:
        """
        self._headless = enable
        enable and self.add(args="--headless=new")

    def set_no_sandbox(self, enable: bool = True):
        """
        设置 no_sandbox

        :param enable: 是否启用
        :return:
        """
        enable and self.add(args="--no-sandbox")

    def set_incognito(self, enable: bool = True):
        """
        启用无痕模式

        新建上下文的话就等于无痕模式了

        :param enable: 是否启用
        :return:
        """
        enable and self.add(args="--incognito")

    def set_ignore_certificate_errors(self, enable: bool = True):
        """
        忽略证书错误

        :param enable: 是否启用
        :return:
        """
        enable and self.add(args="--ignore-certificate-errors")

    def set_disable_images(self, enable: bool = True):
        """
        禁用图片加载

        :param enable: 是否启用
        :return:
        """
        enable and self.add(args="--blink-settings=imagesEnabled=false")

    def set_disable_js(self, enable: bool = True):
        """
        禁用 js 加载

        :param enable: 是否启用
        :return:
        """
        enable and self.add(args="--disable-javascript")

    def set_disable_gpu(self, enable: bool = True):
        """
        禁用 gpu

        :param enable: 是否启用
        :return:
        """
        enable and self.add(args="--disable-gpu")

    def set_disable_extensions(self, enable: bool = True):
        """
        禁用扩展

        :param enable: 是否启用
        :return:
        """
        enable and self.add(args="--disable-extensions")

    def set_disable_software_rasterizer(self, enable: bool = True):
        """
        禁用软件光栅化器

        软件光栅化器是一种渲染技术，用于在没有硬件加速支持的系统上进行图形渲染
        禁用软件光栅化器意味着如果 GPU 不可用，应用程序将不会尝试使用 CPU 作为后备选项

        :param enable: 是否启用
        :return:
        """
        enable and self.add(args="--disable-software-rasterizer")

    def set_start_maximized(self, enable: bool = True):
        """
        设置浏览器启动时最大窗口

        TODO 测试和设置窗口大小会不会有冲突

        :param enable: 是否启用
        """
        enable and self.add(args="--start-maximized")

    """
        属性读取
    """

    @property
    def user_data_dir(self) -> Path:
        return self._user_data_dir

    @property
    def browser_path(self) -> Path:
        return self._browser_path

    @property
    def address(self) -> str:
        if self._ip is None or self._port is None:
            return ""
        return f"{self._ip}:{self._port}"

    @property
    def headless(self) -> bool:
        return self._headless

    @property
    def port(self) -> int:
        return self._port

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def user_agent(self) -> str:
        return self._user_agent

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def proxy(self) -> dict:
        if not self._proxy:
            return {}
        return self._proxy

    @property
    def delete_user_data_dir_when_stop(self) -> bool:
        return self._delete_user_data_dir_when_stop


if __name__ == '__main__':
    opts = BrowserOptions()
    opts.remove("disable")
    print(opts.args)
