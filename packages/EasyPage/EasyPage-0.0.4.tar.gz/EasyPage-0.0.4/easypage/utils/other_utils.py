import asyncio
import functools
import typing
import traceback
from pathlib import Path
from typing import Union


def path_exists(path: str) -> Union[Path, bool]:
    """
    检查一个字符串是否是路径是否存在

    :param path:
    :return:
    """
    try:
        p = Path(path)
        if p.exists():
            return p
    except OSError:
        pass

    return False


def catch_error(f: typing.Callable):
    """
    错误补货装饰器，用于事件触发时将错误抛出，不然 pyee 模块事件执行错误没有报错

    :param f:
    :return:
    """

    def wrapper(*args, **kwargs):
        try:
            # 正常执行函数
            return f(*args, **kwargs)
        except:
            traceback.print_exc()

    return wrapper


# 将普通函数转为异步函数
def to_async(func):
    @functools.wraps(func)
    async def _wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))
        return result

    return _wrapper
