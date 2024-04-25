from typing import Tuple
from easypage.conn import Conn


class Emulation:
    """
        Emulation

        https://chromedevtools.github.io/devtools-protocol/tot/Emulation
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def set_focus_emulation_enabled(
            self,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        焦点模拟，可以模拟键盘事件

        https://chromedevtools.github.io/devtools-protocol/tot/Emulation/#method-setFocusEmulationEnabled

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Emulation.setFocusEmulationEnabled",
            params={
                "enabled": True
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )
