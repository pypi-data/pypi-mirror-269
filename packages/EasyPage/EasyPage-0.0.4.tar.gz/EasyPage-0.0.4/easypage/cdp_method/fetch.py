from typing import Tuple, List
from easypage.conn import Conn


class Fetch:
    """
        Fetch

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def enable(
            self,
            handle_auth_requests: bool = False,
            patterns: List[str] = None,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """

        允许发出 requestPaused 事件

        注意：这会导致请求暂停，需要调用 failRequest、fulfillRequest 或 continueRequest/continueWithAuth 之一

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-enable

        :param handle_auth_requests:
        :param patterns:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return: {"method":"Fetch.requestPaused","params":{"requestId":"interception-job-1.0","request":{"url":"https://www.baidu.com/","method":"GET","headers":{"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36","sec-ch-ua":"\"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"","sec-ch-ua-mobile":"?0","sec-ch-ua-platform":"\"Windows\""},"initialPriority":"VeryHigh","referrerPolicy":"strict-origin-when-cross-origin"},"frameId":"F096060E94EF02389AAE43C27A9F54A4","resourceType":"Document"}}
        """
        if patterns is None:
            patterns = [{"urlPattern": "*"}]

        return self.__conn.send(
            method="Fetch.enable",
            params={
                "handleAuthRequests": handle_auth_requests,
                "patterns": patterns
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def fail_request(
            self,
            request_id: str,
            error_reason: str,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        发出 failRequest 事件

        可能具有以下错误：
            Failed
            Aborted
            TimedOut
            AccessDenied
            ConnectionClosed
            ConnectionReset
            ConnectionRefused
            ConnectionAborted
            ConnectionFailed
            NameNotResolved
            InternetDisconnected
            AddressUnreachable
            BlockedByClient
            BlockedByResponse

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-failRequest

        :param request_id:
        :param error_reason: https://chromedevtools.github.io/devtools-protocol/tot/Network/#type-ErrorReason
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Fetch.failRequest",
            params={
                "requestId": request_id,
                "errorReason": error_reason
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def ful_fill_request(
            self,
            request_id: str,
            resp_code: int,
            resp_headers: dict,
            raise_err: bool = False,
            need_callback: bool = False,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        发出 fulfillRequest 事件（用来提供完整的响应内容）

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-fulfillRequest

        使用 Fetch.fulfillRequest 命令时，您可以提供完整的响应内容，包括状态码、响应头部和响应主体。
        这个命令用于完全替换原始请求的响应，您需要提供响应的所有部分。
        通常在您希望完全替换原始响应内容时使用。

        :param request_id:
        :param resp_code:
        :param resp_headers:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        send_data = {
            'requestId': request_id,
            'responseCode': resp_code,
            'responseHeaders': resp_headers
        }

        send_data.update(kwargs)

        return self.__conn.send(
            method="Fetch.fulfillRequest",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def continue_request(
            self,
            request_id: str,
            raise_err: bool = False,
            need_callback: bool = False,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        发出 continueRequest 事件（用来修改拦截的响应的部分内容）

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-continueRequest

        :param request_id:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        send_data = {
            'requestId': request_id,
        }

        send_data.update(kwargs)

        return self.__conn.send(
            method="Fetch.continueRequest",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def continue_with_auth(
            self,
            request_id: str,
            user: str,
            pwd: str,
            response: str = "ProvideCredentials",
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        发出 continueWithAuth 事件（提供身份验证）

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-continueWithAuth

        authChallengeResponse 参数详解：
        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#type-AuthChallengeResponse

        :param request_id:
        :param user:
        :param pwd:
        :param response:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Fetch.continueWithAuth",
            params={
                "requestId": request_id,
                "authChallengeResponse": {
                    'response': response,  # Default、CancelAuth（取消验证）、ProvideCredentials
                    'username': user,
                    'password': pwd,
                },
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def continue_response(
            self,
            request_id: str,
            raise_err: bool = False,
            need_callback: bool = False,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        发出 continueResponse 事件（用来修改拦截的响应的部分内容）

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-continueResponse

        使用 Fetch.continueResponse 命令时，您可以修改拦截的响应的部分内容，而不是提供完整的响应。
        您可以使用这个命令来修改响应头部、响应状态码和响应主体等部分内容，而不需要提供完整的响应。
        这个命令用于对拦截的响应进行部分修改，而不需要重新构造整个响应。
        通常在您只需要修改响应的部分内容而不是完全替换时使用。

        :param request_id:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        send_data = {
            'requestId': request_id,
        }

        send_data.update(kwargs)

        return self.__conn.send(
            method="Fetch.continueResponse",
            params=send_data,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def get_response_body(
            self,
            request_id: str,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        获得响应体

        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-getResponseBody

        :param request_id:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="Fetch.getResponseBody",
            params={
                "requestId": request_id
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )
