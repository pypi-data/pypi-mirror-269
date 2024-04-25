from typing import Tuple
from easypage.conn import Conn


class Input:
    """
        Input

        https://chromedevtools.github.io/devtools-protocol/tot/Input
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def dispatch_key_event(
            self,
            event_type: str,
            raise_err: bool = False,
            need_callback: bool = False,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        执行键盘的命令

        学习链接：https://chromedevtools.github.io/devtools-protocol/tot/Input/#method-dispatchKeyEvent

        :param event_type: 如：keyDown, keyUp, rawKeyDown, char
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        send_data = {
            "type": event_type,
        }
        send_data.update(kwargs)

        if "key" in send_data:
            send_data['key'] = "Key " + send_data['key'].upper()

        return self.__conn.send(
            method="Input.dispatchKeyEvent",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def dispatch_mouse_event(
            self,
            event_type: str,
            x: int,
            y: int,
            button: str = "none",
            raise_err: bool = False,
            need_callback: bool = False,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        执行鼠标的命令

        学习链接：https://chromedevtools.github.io/devtools-protocol/tot/Input/#method-dispatchMouseEvent

        :param event_type: 如：mousePressed, mouseReleased, mouseMoved, mouseWheel
        :param x: 点击的坐标
        :param y: 点击的坐标
        :param button: 代表鼠标的按键，如：none（不触发按键，代表光标）, left（左击）, middle（滚轮）, right（右击）, back（后退）, forward（前进）
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        send_data = {
            "type": event_type,
            "x": x,
            "y": y,
            "button": button,
        }
        send_data.update(kwargs)

        return self.__conn.send(
            method="Input.dispatchMouseEvent",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )
