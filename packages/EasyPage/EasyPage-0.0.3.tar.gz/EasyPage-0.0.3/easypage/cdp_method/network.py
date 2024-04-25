from typing import Tuple
from easypage.conn import Conn


class NetWork:
    """
        NetWork

        https://chromedevtools.github.io/devtools-protocol/tot/Network
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def enable(
            self,
            raise_err: bool = False,
            need_callback: bool = False,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        启用网络跟踪，网络事件现在将传递到客户端。

        https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-enable

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Network.enable",
            params=kwargs,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def set_extra_http_headers(
            self,
            headers: dict,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        指定是否始终随此页面的请求发送额外的 HTTP 标头。

        https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-setExtraHTTPHeaders

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :param headers:
        :return:
        """
        return self.__conn.send(
            method="Network.setExtraHTTPHeaders",
            params={
                "headers": headers
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def set_user_agent_override(
            self,
            user_agent: str,
            raise_err: bool = False,
            need_callback: bool = False,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        允许使用给定的字符串覆盖用户代理。

        https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-setUserAgentOverride

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :param user_agent:
        :return:
        """
        send_data = {
            'userAgent': user_agent
        }

        send_data.update(kwargs)

        return self.__conn.send(
            method="Network.setUserAgentOverride",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def set_cache_disabled(
            self,
            cache_disabled: bool = True,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        禁用缓存

        https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-setCacheDisabled

        :param cache_disabled:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Network.setCacheDisabled",
            params={
                "cacheDisabled": cache_disabled
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )
