from typing import Tuple
from easypage.conn import Conn
from easypage.utils import other_utils


class Runtime:
    """
        Runtime

        https://chromedevtools.github.io/devtools-protocol/tot/Runtime
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def evaluate(
            self,
            js: str,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        执行 js 脚本

        学习链接：https://chromedevtools.github.io/devtools-protocol/tot/Runtime/#method-evaluate

        :param js: 路径或者 js 字符串
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return: {'id': 1, 'result': {'result': {'type': 'number', 'value': 2, 'description': '2'}}}
        """
        if other_utils.path_exists(js):
            with open(js, "r") as f:
                js = f.read()

        send_data = {
            'expression': js,
            "returnByValue": False,
            "awaitPromise": True,
            "userGesture": True
        }
        send_data.update(kwargs)

        return self.__conn.send(
            method="Runtime.evaluate",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def call_function_on(
            self,
            js: str,
            object_id: str,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        执行 js 脚本，可以指定 objectId 这样就相当于上下文是元素自身了

        学习链接：https://chromedevtools.github.io/devtools-protocol/tot/Runtime/#method-callFunctionOn

        :param js: 路径或者 js 字符串
        :param object_id: 对应的对象（相当于上下文）
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        if other_utils.path_exists(js):
            with open(js, "r") as f:
                js = f.read()

        send_data = {
            'functionDeclaration': js,
            'objectId': object_id,
            "awaitPromise": True,
            "userGesture": True
        }

        send_data.update(kwargs)

        return self.__conn.send(
            method="Runtime.callFunctionOn",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def get_properties(
            self,
            object_id: str,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        获取给定对象的属性

        https://chromedevtools.github.io/devtools-protocol/tot/Runtime/#method-getProperties

        :param object_id:
        :param kwargs:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        send_data = {
            "objectId": object_id,
        }

        send_data.update(kwargs)

        return self.__conn.send(
            method="Runtime.getProperties",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )
