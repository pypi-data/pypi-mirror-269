import socket
from pathlib import Path
from platform import system
from typing import List, Union


def find_browser_path() -> str:
    """
    寻找浏览器的路径

    :return:
    """
    # 通过 which 获取
    from shutil import which

    which_list = [
        'chrome',
        'chromium',
        'google-chrome',
        'google-chrome-stable',
        'google-chrome-unstable',
        'google-chrome-beta',
    ]
    for wl in which_list:
        path = which(wl)
        if path:
            return path

    # 默认路径获取
    sys_type = system().lower()
    if sys_type in ('macos', 'darwin'):
        p = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        return p if Path(p).exists() else None

    elif sys_type == 'linux':
        paths = ('/usr/bin/google-chrome', '/opt/google/chrome/google-chrome',
                 '/user/lib/chromium-browser/chromium-browser')
        for p in paths:
            if Path(p).exists():
                return p
        return

    elif sys_type == 'windows':
        # 通过注册表获取
        from winreg import OpenKey, EnumValue, CloseKey, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, KEY_READ

        txt = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
        for find_key in [HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE]:
            try:
                key = OpenKey(find_key, txt, reserved=0, access=KEY_READ)
                k = EnumValue(key, 0)
                CloseKey(key)
                if k[1]:
                    return k[1]
            except (FileNotFoundError, OSError):
                pass
    else:
        raise Exception(f"不受支持的系统：{sys_type}")


def find_free_port() -> int:
    """
    寻找一个空闲端口

    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定到本地地址和端口，让系统自动分配端口
    sock.bind(('127.0.0.1', 0))

    # 获取分配的端口
    port = sock.getsockname()[1]

    sock.close()

    return port


def port_in_use(port, ip: str = '127.0.0.1') -> bool:
    """
    判断指定端口是否被占用

    :param port:
    :param ip:
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((ip, port))
    sock.close()

    return result == 0


def parse_driver_id(data: Union[List[dict], dict]) -> List[str]:
    """
    返回 id 列表

    :param data:
    :return:
    """
    if not isinstance(data, list):
        data = [data]

    result = []
    for d in data:
        if d.get("webSocketDebuggerUrl"):
            result.append(d['webSocketDebuggerUrl'].split('/')[-1])

    return result


def parse_box_center_coordinate(data: list) -> tuple:
    """
    根据给定的目标，计算中心点坐标

    :param data: [844, 222.703125, 952, 222.703125, 952, 266.703125, 844, 266.703125]
    :return:
    """
    # 提取四个顶点的坐标
    x1, y1, x2, y2, x3, y3, x4, y4 = data

    # 计算矩形的左上角和右下角坐标
    left = min(x1, x4)
    right = max(x2, x3)
    top = min(y1, y2)
    bottom = max(y3, y4)

    # 计算矩形中心点的坐标
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2

    return center_x, center_y


if __name__ == "__main__":
    free_port = find_free_port()
    print("Free port:", free_port)

    port_to_check = 9222
    if port_in_use(port_to_check):
        print(f"Port {port_to_check} is in use.")
    else:
        print(f"Port {port_to_check} is free.")
