from typing import Tuple
from easypage.conn import Conn


class Security:
    """
        Storage

        https://chromedevtools.github.io/devtools-protocol/tot/Security
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def enable(
            self,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        启用安全

        https://chromedevtools.github.io/devtools-protocol/tot/Security/#method-enable

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Security.enable",
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def disable(
            self,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        禁用安全

        https://chromedevtools.github.io/devtools-protocol/tot/Security/#method-disable

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Security.disable",
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def set_ignore_certificate_errors(
            self,
            ignore: bool = True,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        忽略证书错误

        https://chromedevtools.github.io/devtools-protocol/tot/Security/#method-setIgnoreCertificateErrors

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :param ignore:
        :return:
        """
        return self.__conn.send(
            method="Security.setIgnoreCertificateErrors",
            params={
                "ignore": ignore
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )
