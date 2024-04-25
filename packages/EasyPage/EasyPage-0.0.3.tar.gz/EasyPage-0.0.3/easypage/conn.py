"""
    使用了 EventEmitter 作为事件管理

    # 创建事件监听案例
    async def intercept(kwargs) -> None:
        print(kwargs)
        interception_id = kwargs["interceptionId"]

        await page_conn.send(
            method="Network.continueInterceptedRequest",
            params={"interceptionId": interception_id},
        )

    page_conn.on("Network.requestIntercepted", lambda event: loop.create_task(intercept(event)))

    异步这里代码结构有问题，仅针对 send 方法
        事件监听，监听到事件之后将会触发 loop.run_until_complete 操作
        同时同步程序也会有 loop.run_until_complete 就会造成报错：This event loop is already running
        需要对代码结构做处理，如有统一的事件发送地址，或者使用类似队列的结构
"""
import json
import time
import typing
import asyncio
import threading
import traceback
import websocket
import websockets
from threading import Lock
from easypage import errors
from pyee import EventEmitter
from easypage.logger import logger
from queue import SimpleQueue, Empty
from websockets.legacy import client

TYPE_PAGE = "page"
TYPE_BROWSER = "browser"

DRIVER_TYPE = typing.Union[
    TYPE_BROWSER,
    TYPE_PAGE
]


class ConnAsync(EventEmitter):
    def __init__(self, address: str, driver_type: DRIVER_TYPE, driver_id: str, loop: asyncio.AbstractEventLoop = None):
        """
        # 页面连接
        ws://127.0.0.1:9223/devtools/page/87B827CF2CAF710C997699F858467545

        # 浏览器连接
        ws://127.0.0.1:9223/devtools/browser/0909caac-09eb-4f48-a481-5de5decb3583

        :param loop: 事件循环（没传的话，会自动创建）
        :param address: 连接地址，如：127.0.0.1:9223
        :param driver_type: 控制类型，如：TYPE_PAGE
        :param driver_id: 对应 id，如：87B827CF2CAF710C997699F858467545
        """
        super().__init__()
        self.__loop = loop or asyncio.get_event_loop()
        self.address = address
        self.driver_id = driver_id
        self.driver_type = driver_type
        self.driver_url = f"ws://{address}/devtools/{driver_type}/{driver_id}"

        self.__lock = Lock()
        self.__id = 0
        self.__events = {}  # 存储事件
        self.__callbacks = {}  # 管理所有回调
        self.__connected = False  # 是否已经连接上（client.WebSocketCommonProtocol 是否已创建）
        self.__ws = self.new_conn()  # ws 连接
        self.__conn: client.WebSocketCommonProtocol = None  # type: ignore # 实际操作的连接
        self.__recv_fut = self.__loop.create_task(self.__recv())  # 异步消息接收

    def new_conn(self) -> client.Connect:
        """
        创建新的 ws 连接，使用的时候需要创建 client.WebSocketCommonProtocol

        :return:
        """
        return client.connect(
            uri=self.driver_url,
            max_size=None,
            loop=self.__loop,
            ping_interval=None,
            ping_timeout=None
        )

    def send(self, method: str, params: dict = None, raise_err: bool = False) -> typing.Tuple[bool, dict]:
        """
        同步发送消息

        使用：status, value = send(method="", raise_err=False, params={})

        返回的结果是有两个值：
            - status 表示当前消息是否有错误发生（raise_err 为 True 时直接抛出）
            - value 是对应浏览器返回的消息，是一个 dict

        :param method:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param params:
        :return
        """
        # 获得结果
        callback = self.send_async(
            method=method,
            raise_err=raise_err,
            params=params
        )

        # 在同步上下文中运行异步函数
        status, value = self.__loop.run_until_complete(asyncio.wait_for(callback, timeout=10))

        return status, value

    def send_async(self, method: str, raise_err: bool = False, params: dict = None) -> typing.Awaitable:
        """
        异步发送消息，返回一个需要 await 等待的对象

        使用：status, value = send(method="", raise_err=False, params={})

        返回的结果是有两个值：
            - status 表示当前消息是否有错误发生（raise_err 为 True 时直接抛出）
            - value 是对应浏览器返回的消息，是一个 dict

        :param method:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param params:
        :return
        """
        # 发送消息
        msg = {
            "id": self.__next_id,
            "method": method,
            "params": params or dict()
        }
        self.__loop.create_task(self.__send(msg))

        # 构建 Future 对象返回
        callback = self.__loop.create_future()
        self.__callbacks[msg["id"]] = callback
        callback.raise_err: bool = raise_err  # type: ignore
        callback.error: Exception = errors.CDPRecvMsgError()  # type: ignore
        callback.method: str = method  # type: ignore
        return callback

    async def __send(self, msg: dict) -> None:
        """
        消息发送

        :param msg:
        :return:
        """
        # 等待连接建立
        while not self.__connected:
            await asyncio.sleep(0)

        # 发送消息
        msg_id = msg["id"]
        msg = json.dumps(msg, ensure_ascii=False)
        logger.debug("[SEND] {}", msg)

        try:
            await self.__conn.send(msg)
        except (websockets.ConnectionClosed, websockets.ConnectionClosedOK):
            logger.warning(f"连接已关闭：{self.driver_url}")

            # 获取回调对象并设置结果
            callback = self.__callbacks.get(msg_id, None)
            if callback and not callback.done():
                callback.set_result((False, dict()))
                await self.close()

    async def __recv(self) -> None:
        """
        接收消息

        :return:
        """
        async with self.__ws as conn:
            self.__conn = conn
            self.__connected = True
            while self.__connected:
                try:
                    msg = await self.__conn.recv()
                    if not msg:
                        break
                    await self.__onmessage(msg=msg)
                except (websockets.ConnectionClosed, ConnectionResetError):
                    logger.warning(f"连接已关闭：{self.driver_url}")
                    break
                await asyncio.sleep(0)

    async def __onmessage(self, msg: str) -> None:
        """
        接收到的消息处理

        :param msg:
        :return:
        """
        await asyncio.sleep(0)
        if "Not allowed" in msg:
            logger.warning(f"当前 driver 不支持该命令，请切换 driver，当前 driver 类型：{self.driver_type}")
        msg = json.loads(msg)

        # 消息回调
        if msg.get('id') in self.__callbacks:
            callback = self.__callbacks.pop(msg['id'])
            if msg.get('error'):
                logger.warning("[RECV] {}", msg)
                if callback.raise_err:
                    callback.error.args = (f"接收到错误消息：{msg['error']}",)  # 设置错误消息
                    callback.set_exception(callback.error)
                else:
                    callback.set_result((False, msg.get('error')))
            else:
                logger.debug("[RECV] {}", msg)
                callback.set_result((True, msg.get('result')))

        # 事件触发
        else:
            logger.debug("[RECV] {}", msg)
            method = msg.get('method', '')
            params = msg.get('params', {})
            self.emit(method, **params)
            print("接收到事件 -> ", method, self.__events.get(method))
            # if self.__events.get(method):
            #     for f in self.__events[method]:
            #         f(**params)

    # def on(self, event: str, f: typing.Callable):
    #     print("event -> ", event)
    #     if event not in self.__events:
    #         self.__events[event] = set()
    #
    #     self.__events[event].add(f)

    async def close(self) -> None:
        """
        关闭连接

        :return:
        """
        self.__connected = False
        await asyncio.sleep(0)

        # 未获取的结果设置异常
        for cb in self.__callbacks.values():
            if cb.raise_err:
                cb.error.args = (f'连接关闭：{cb.method}',)  # 设置错误消息
                cb.set_exception(cb.error)
            else:
                cb.set_result((False, f'连接关闭：{cb.method}'))

        self.__callbacks.clear()

        # 关闭连接
        if self.__conn:
            await self.__conn.close()
            self.__conn = None

        # 取消等待
        if not self.__recv_fut.done():
            self.__recv_fut.cancel()

    @property
    def __next_id(self) -> int:
        """
        获取消息 id

        :return:
        """
        self.__lock.acquire(timeout=2)
        self.__id += 1
        self.__lock.release()
        return self.__id


class Conn(EventEmitter):

    def __init__(self, address: str, driver_type: DRIVER_TYPE, driver_id: str):
        """
        # 页面连接
        ws://127.0.0.1:9223/devtools/page/87B827CF2CAF710C997699F858467545

        # 浏览器连接
        ws://127.0.0.1:9223/devtools/browser/0909caac-09eb-4f48-a481-5de5decb3583

        :param address: 连接地址，如：127.0.0.1:9223
        :param driver_type: 控制类型，如：TYPE_PAGE
        :param driver_id: 对应 id，如：87B827CF2CAF710C997699F858467545
        """
        super().__init__()
        self.address = address
        self.driver_id = driver_id
        self.driver_type = driver_type
        self.driver_url = f"ws://{address}/devtools/{driver_type}/{driver_id}"

        self.__lock = threading.Lock()
        self.__id: int = 0
        self.__stop: bool = False
        self.__ws: WebSocket = None  # type:ignore
        self.__result_monitor = {}  # 存储结果
        self.__new_conn()

    def __new_conn(self):
        """
        与浏览器建立连接

        :return:
        """
        self.__ws = websocket.create_connection(
            url=self.driver_url,
            enable_multithread=True,
            suppress_origin=True
        )
        threading.Thread(target=self.__recv_result, daemon=True).start()

    def send(
            self,
            method: str,
            params: dict = None,
            raise_err: bool = False,
            need_callback: bool = True
    ) -> typing.Tuple[bool, dict]:
        """
        同步发送消息

        使用：status, value = send(method="", raise_err=False, params={})

        返回的结果是有两个值：
            - status 表示当前消息是否有错误发生（raise_err 为 True 时直接抛出）
            - value 是对应浏览器返回的消息，是一个 dict

        :param method:
        :param params:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return
        """
        # 构建消息
        msg = {
            "id": self.__get_id,
            "method": method,  # 在此示例中启用网络事件
            "params": params
        }

        self.__result_monitor[msg["id"]] = SimpleQueue()

        msg_json = json.dumps(msg)
        logger.debug("[SEND] {}", msg_json)

        # 发送信息
        try:
            self.__ws.send(msg_json)

            if not need_callback:
                return True, dict()

            # 等待信息接收
            start_time = time.time()
            while not self.__stop:
                if self.closed():
                    break

                try:
                    recv_msg = self.__result_monitor[msg["id"]].get(timeout=0.1)  # 短等待，避免有问题卡着
                    if "result" in recv_msg:
                        return True, recv_msg["result"]
                    elif "error" in recv_msg:
                        if raise_err:
                            raise errors.CDPRecvErrorMsg(recv_msg["error"])
                        return False, recv_msg["error"]

                    logger.error("没有结果：{}", recv_msg)
                except Empty:
                    if time.time() - start_time >= 30:
                        self.__remove_result(msg_id=msg['id'])
                        if raise_err:
                            raise errors.CDPRecvTimeout(msg)
                        logger.error("接收超时：{}", msg)
                        break
        except (errors.CDPRecvTimeout, errors.CDPRecvErrorMsg):
            raise
        except websocket.WebSocketConnectionClosedException:
            logger.warning("连接已断开：{}", self.driver_url)
        except:
            traceback.print_exc()

        return False, dict()

    def __recv_result(self):
        """
        接收消息、事件处理

        :return:
        """
        while not self.__stop:
            try:
                msg = self.__ws.recv()
                logger.debug("[RECV] {}", msg)
                msg = json.loads(msg)
            except websocket.WebSocketTimeoutException:
                continue
            except (websocket.WebSocketConnectionClosedException, ConnectionResetError):
                logger.warning("连接已断开：{}", self.driver_url)
                return
            except Exception:
                if self.__stop:
                    return
                else:
                    self.__stop = True
                    raise

            # 消息处理
            if msg.get("id") and msg.get("id") in self.__result_monitor:
                if msg.get("error"):
                    logger.error("[RECV] {}", msg["error"])
                self.__add_result(msg_id=msg["id"], result=msg)
            elif "method" in msg:
                method = msg.get("method", "")
                params = msg.get("params", {})
                self.emit(method, **params)

    def closed(self) -> bool:
        """
        判断连接是否断开，同时做一点处理

        :return:
        """
        status = self.__ws.connected
        if not status:
            self.__stop = True

        return not status

    def close(self):
        """
        停止运行

        :return:
        """
        self.__stop = True
        self.__ws.close()

    def __add_result(self, msg_id: int, result: dict):
        """
        添加监控结果

        :param msg_id:
        :param result:
        :return:
        """
        if msg_id in self.__result_monitor:
            self.__result_monitor[msg_id].put(result)

    def __remove_result(self, msg_id: int):
        """
        移除监控

        :param msg_id:
        :return:
        """
        if msg_id in self.__result_monitor:
            del self.__result_monitor[msg_id]

    @property
    def __get_id(self):
        """
        获取一个消息 id

        :return:
        """
        self.__lock.acquire(timeout=2)
        self.__id += 1
        self.__lock.release()

        return self.__id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
