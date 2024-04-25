from typing import Union, List


class URLError(Exception):
    def __init__(self, url: str):
        super().__init__("该 url 似乎非法：{}".format(url))


class ProxySetError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class Timeout(Exception):
    def __init__(self, msg: str):
        super().__init__("超时：{}".format(msg))


class ConnectTimeout(Exception):
    def __init__(self, address: str):
        super().__init__("连接超时：{}".format(address))


class BrowserConnectTimeout(Exception):
    def __init__(self, address: str):
        super().__init__("浏览器连接超时：{}".format(address))


class CDPConnClosed(Exception):
    def __init__(self, msg: str):
        super().__init__("连接关闭：{}".format(msg))


# 接收到的消息有错误时触发
class CDPRecvErrorMsg(Exception):
    def __init__(self, msg: str):
        super().__init__("接收到错误消息：{}".format(msg))


class CDPRecvTimeout(Exception):
    def __init__(self, msg: dict):
        super().__init__("接收消息超时：{}".format(msg))


"""
    Element
"""


class ElementWaitTimeout(Exception):
    def __init__(self, ele: Union[List[str], str]):
        super().__init__("元素等待超时：{}".format(ele))


class ElementNotFound(Exception):
    def __init__(self, ele: str):
        super().__init__("没有找到元素：{}".format(ele))
