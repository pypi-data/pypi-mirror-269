from typing import Tuple
from easypage.conn import Conn


class Dom:
    """
        Dom

        https://chromedevtools.github.io/devtools-protocol/tot/Dom
    """

    def __init__(self, conn: Conn):
        self.__conn = conn

    def enable(
            self,
            raise_err: bool = False,
            need_callback: bool = False,
    ) -> Tuple[bool, dict]:
        """
        启用 DOM 功能（查询元素、修改元素属性等）

        https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-enable

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="DOM.enable",
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def get_document(
            self,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        获取当前页面的完整 DOM 结构（DOM的根节点）

        学习地址：https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-getDocument

        注意：
        - 页面一但有变动就需要加载，否则获取的数据不准
        - 这里仅仅是获取了 backendNodeId

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return: {'nodeId': 1, 'backendNodeId': 1, 'nodeType': 9, 'nodeName': '#document', 'localName': '', 'nodeValue': '', 'childNodeCount': 1, 'children': [{'nodeId': 2, 'parentId': 1, 'backendNodeId': 2, 'nodeType': 1, 'nodeName': 'HTML', 'localName': 'html', 'nodeValue': '', 'childNodeCount': 2, 'children': [{'nodeId': 3, 'parentId': 2, 'backendNodeId': 3, 'nodeType': 1, 'nodeName': 'HEAD', 'localName': 'head', 'nodeValue': '', 'childNodeCount': 0, 'attributes': []}, {'nodeId': 4, 'parentId': 2, 'backendNodeId': 4, 'nodeType': 1, 'nodeName': 'BODY', 'localName': 'body', 'nodeValue': '', 'childNodeCount': 0, 'attributes': []}], 'attributes': [], 'frameId': '9958473737B20C99BBC0BAE47BA5F6E4'}], 'documentURL': 'about:blank', 'baseURL': 'about:blank', 'xmlVersion': '', 'compatibilityMode': 'QuirksMode'}
        """
        return self.__conn.send(
            method="DOM.getDocument",
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def query_selector(
            self,
            selector: str,
            node_id: int = None,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        选择元素

        https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-querySelector

        :param selector: 选择器（支持 css、xpath）
        :param node_id: 节点 id（基于某个节点查找时需要）
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        # 没有节点 id 的话，获取根节点的 id
        if not node_id:
            status, root = self.get_document()
            if not status or not root:
                return status, root

            node_id = root['root']['nodeId']

        return self.__conn.send(
            method="DOM.querySelector",
            params={
                "nodeId": node_id,
                "selector": selector
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def query_selector_all(
            self,
            selector: str,
            node_id: int = None,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        选择多个元素

        https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-querySelectorAll

        :param selector: 选择器（支持 css、xpath）
        :param node_id: 节点 id（基于某个节点查找时需要）
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        # 没有节点 id 的话，获取根节点的 id
        if not node_id:
            status, root = self.get_document()
            if not status or not root:
                return status, root

            node_id = root['root']['nodeId']

        return self.__conn.send(
            method="DOM.querySelectorAll",
            params={
                "nodeId": node_id,
                "selector": selector
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def resolve_node(
            self,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        将给定的 DOM 节点 ID 解析为对应的 JavaScript 对象

        学习地址：https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-resolveNode

        建议传参：backendNodeId，不行的话 nodeId 也行

        可以获取到 objectId

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return: {"object":{"type":"object","subtype":"node","className":"HTMLDocument","description":"#document","objectId":"5606348279645422547.1.1"}}
        """
        return self.__conn.send(
            method="DOM.resolveNode",
            params=kwargs,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def describe_node(
            self,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        根据 nodeId 处理返回 dict 对象

        可以根据 nodeId、backendNodeId、objectId 获取

        学习地址：https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-describeNode

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return: {'node': {'nodeId': 73, 'backendNodeId': 122, 'nodeType': 1, 'nodeName': 'IFRAME', 'localName': 'iframe', 'nodeValue': '', 'childNodeCount': 0, 'attributes': ['src', 'https://kunpeng-sc.csdnimg.cn/?timestamp=1645783940/#/preview/1012105?positionId=588&adBlockFlag=0&adId=1050061&queryWord=&spm=3001.5907&articleId=0', 'frameborder', '0', 'width', '100%', 'height', '400px', 'scrolling', 'no'], 'frameId': '216187998879F6BA0E5C47C69713FE99'}}
        """
        return self.__conn.send(
            method="DOM.describeNode",
            params=kwargs,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def get_attributes(
            self,
            node_id: int,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> Tuple[bool, dict]:
        """
        获取属性

        学习地址：https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-getAttributes

        需要通过以下方法转换成需要的字典
            attrs_list = attributes["attributes"]
            attrs = dict(zip(attrs_list[::2], attrs_list[1::2]))

        :param node_id:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="DOM.getAttributes",
            params={
                "nodeId": node_id
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def focus(
            self,
            raise_err: bool = False,
            need_callback: bool = False,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        聚焦

        可以根据 nodeId、backendNodeId、objectId 获取

        学习链接：https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-focus

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method='DOM.focus',
            params=kwargs,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def set_attribute_value(
            self,
            name: str,
            value: str,
            node_id: int,
            raise_err: bool = False,
            need_callback: bool = False
    ) -> Tuple[bool, dict]:
        """
        修改属性

        https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-setAttributeValue

        :param name: 属性名称
        :param value: 属性值
        :param node_id:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method='DOM.setAttributeValue',
            params={
                "nodeId": node_id,
                "name": name,
                "value": value,
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def get_box_model(
            self,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        返回给定节点的框
        返回的比如 content 有 4 个坐标，分别是
        - 左上顶点
        - 右上顶点
        - 右下顶点
        - 左下顶点

        可以根据 nodeId、backendNodeId、objectId 获取

        学习链接：https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-getBoxModel

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method='DOM.getBoxModel',
            params=kwargs,
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def get_frame_owner(
            self,
            frame_id: str,
            raise_err: bool = False,
            need_callback: bool = True
    ) -> Tuple[bool, dict]:
        """
        获取 iframe 的 backendNodeId、nodeId

        学习链接:https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-getFrameOwner

        :param frame_id:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="DOM.getFrameOwner",
            params={
                "frameId": frame_id
            },
            raise_err=raise_err,
            need_callback=need_callback,
        )

    def get_outer_html(
            self,
            raise_err: bool = False,
            need_callback: bool = True,
            **kwargs
    ) -> Tuple[bool, dict]:
        """
        获取页面含标签的内容

        可以根据 nodeId、backendNodeId、objectId 获取

        https://chromedevtools.github.io/devtools-protocol/tot/DOM/#method-getOuterHTML

        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return:
        """
        return self.__conn.send(
            method="DOM.getOuterHTML",
            params=kwargs,
            raise_err=raise_err,
            need_callback=need_callback,
        )
