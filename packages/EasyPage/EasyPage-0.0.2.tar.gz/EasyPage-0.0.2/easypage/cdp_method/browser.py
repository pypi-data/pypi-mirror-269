from typing import Tuple

from easypage.conn import Conn


class Browser:
    """
        Browser

        https://chromedevtools.github.io/devtools-protocol/tot/Browser
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def version(
            self,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        获取浏览器的信息

        https://chromedevtools.github.io/devtools-protocol/tot/Browser/#method-getVersion

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Browser.getVersion",
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def close(
            self,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        退出浏览器

        https://chromedevtools.github.io/devtools-protocol/tot/Browser/#method-close

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Browser.close",
            raise_err=raise_err,
            need_callback=need_callback,
        )
