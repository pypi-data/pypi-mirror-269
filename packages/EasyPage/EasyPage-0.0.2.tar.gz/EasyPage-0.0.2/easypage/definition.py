"""
    定义类型
"""
import sys
from typing import Optional

# 版本兼容
if sys.version_info >= (3, 8):
    from typing import Literal, TypedDict
else:
    from typing_extensions import Literal, TypedDict


class Proxy(TypedDict, total=False):
    server: str
    bypass: Optional[str]  # Optional 表示可以为 None
    user: Optional[str]
    pwd: Optional[str]
