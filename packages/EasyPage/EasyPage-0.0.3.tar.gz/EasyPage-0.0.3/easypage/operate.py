"""
    一些浏览器上面的操作
"""
import time
import requests
from easypage import errors
from subprocess import Popen
from easypage import settings
from easypage.logger import logger
from easypage.utils import browser_utils
from easypage.options import BrowserOptions


def browser(address: str) -> dict:
    """
    获取浏览器信息

    :param address:
    :return:
    """
    resp = requests.get(
        url=f'http://{address}/json/version',
        headers={
            'Connection': 'close'
        },
        timeout=10,
    )

    if resp.status_code != 200:
        raise Exception("浏览器连接失败！")

    return resp.json()


def pages(address: str) -> list:
    """
    获取所有的页面信息

    :param address:
    :return:
    """
    resp = requests.get(
        url=f'http://{address}/json',
        headers={
            'Connection': 'close'
        },
        timeout=10,
    )

    return list(filter(
        lambda i: i['type'] in ('page') and not i['url'].startswith('devtools://'),
        resp.json()
    ))


def new_browser(opts: BrowserOptions, check_port_use: bool = True):
    """
    新建浏览器

    :param opts:
    :param check_port_use: 检测端口使用状态
    :return:
    """
    # 获取路径
    browser_path = opts.browser_path or browser_utils.find_browser_path()
    if not browser_path:
        raise FileNotFoundError("浏览器执行路径未找到！")
    logger.debug("本次浏览器连接路径：{}", browser_path)

    if settings.SYSTEM_TYPE == "linux":
        if not opts.exists("--no-sandbox"):
            opts.add("--no-sandbox")
        if not opts.headless:
            logger.warning("当前系统为 linux 但是未设置 --headless")

    # 判断端口使用状态
    port = opts.port or settings.BROWSER_START_PORT
    if check_port_use:
        if browser_utils.port_in_use(port):
            port = browser_utils.find_free_port()
            opts.set_address(ip=opts.ip or settings.BROWSER_START_IP, port=port)
            logger.warning("当前端口被占用，已启用随机端口：{}", port)

    # 判断用户文件夹（不创建的话，会和已有的混在一起导致异常：）
    if not opts.user_data_dir:
        opts.set_user_data_dir(path=settings.USER_DATA_DIR + str(opts.port), delete_if_exists=True)
        logger.debug("未设置用户文件夹，已使用默认路径：{}", opts.user_data_dir)

    # 加入插件
    if opts.extensions:
        opts.add(f"--load-extension={','.join(opts.extensions)}")

    # headless 判断（隐私模式没加 ua 的话，会导致部分网站通过 ua 检测出来：Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/125.0.0.0 Safari/537.36）
    if opts.headless and not opts.user_agent:
        opts.set_user_agent(user_agent=settings.USER_AGENT)

    # 启动浏览器
    logger.debug("本次浏览器连接端口：{}", opts.port)
    arguments = [str(browser_path), f'--remote-debugging-address={opts.ip}', f'--remote-debugging-port={opts.port}']
    arguments.extend(opts.args)

    try:
        return Popen(arguments, shell=False)
    except:
        logger.error("浏览器启动失败！")
        raise


def wait_connection(opts: BrowserOptions):
    """
    等待连接

    :param opts:
    :return:
    """
    start_time = time.time()

    while time.time() - start_time < opts.timeout:
        if test_connection(opts):
            return

    raise errors.BrowserConnectTimeout(opts.address)


def test_connection(opts: BrowserOptions) -> bool:
    """
    测试连通性

    :param opts:
    :return:
    """
    try:
        resp = requests.get(
            url=f'http://{opts.address}/json/version',
            headers={
                'Connection': 'close'
            },
            timeout=30,
        )
        if resp.status_code == 200:
            return True
    except:
        pass

    return False
