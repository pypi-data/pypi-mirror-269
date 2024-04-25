from typing import Tuple
from easypage.conn import Conn


class Storage:
    """
        Storage

        https://chromedevtools.github.io/devtools-protocol/tot/Storage
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def get_cookies(
            self,
            context_id: str,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        获取 同一个 Context 下的 cookies

        https://chromedevtools.github.io/devtools-protocol/tot/Storage/#method-getCookies

        :param context_id:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return: {'cookies': [{'name': '', 'value': '', 'domain': '', 'path': '', 'expires': -1, 'size': 161, 'httpOnly': True, 'secure': True, 'session': True, 'sameSite': 'Strict', 'priority': 'Medium', 'sameParty': False, 'sourceScheme': 'Secure', 'sourcePort': 443}]}
        """
        return self.__conn.send(
            method="Storage.getCookies",
            params={
                "browserContextId": context_id
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )
