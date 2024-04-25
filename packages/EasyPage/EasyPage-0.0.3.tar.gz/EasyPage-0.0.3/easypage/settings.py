"""
    默认公共配置，不做修改
"""
import sys
import logging
from typing import List

SYSTEM_TYPE: str = sys.platform.lower()  # 系统类型
BROWSER_START_IP: str = "127.0.0.1"  # 浏览器启动 ip
BROWSER_START_PORT: int = 9876  # 浏览器启动端口
BROWSER_START_ARGS: List[str] = [
    "--hide-crash-restore-bubble",  # 隐藏崩溃恢复提示泡泡
    "--no-default-browser-check",  # 禁用默认浏览器检查
    "--disable-features=PrivacySandboxSettings4",  # 禁用隐私沙箱设置的特定功能
    "--no-first-run",  # 禁用“首次运行”体验
    "--disable-infobars",  # 启动 Chrome 浏览器时禁用信息栏功能
    "--disable-suggestions-ui",  # 禁用建议功能的用户界面
    "--disable-background-timer-throttling",  # 禁用后台定时器的节流功能
    "--disable-breakpad",  # 禁用 Breakpad 异常报告系统
    "--disable-browser-side-navigation",  # 禁用浏览器端的页面导航，会向服务器发送完整的请求，然后加载新的页面
    "--disable-client-side-phishing-detection",  # 禁用钓鱼检测
    "--disable-default-apps",  # 禁用默认应用程序（不再自动使用系统中配置的默认应用程序，而是使用 Chrome 自带的相应功能或者行为）
    "--disable-dev-shm-usage",  # 禁用共享内存（容器化的场景下会对共享内存限制，可能导致无法正常工作，需要禁用）
    "--disable-features=site-per-process",  # 禁用站点隔离，减少资源消耗（所有的网站内容将会在同一个进程中运行）
    "--disable-hang-monitor",  # 禁用挂起监视器功能
    "--disable-popup-blocking",  # 禁用弹出窗口阻止功能
    "--disable-prompt-on-repost",  # 禁用在重新提交 POST 请求时出现的提示（如刷新的时候提交表单的情况）
    "--disable-sync",  # 禁用浏览器账户同步功能
    "--disable-translate",  # 禁用翻译功能
    "--metrics-recording-only",  # 启动 Chrome 浏览器时，浏览器将会在后台运行，但不会显示浏览器界面，也不会加载任何网页
    "--safebrowsing-disable-auto-update",  # 禁用浏览器自动更新
    "--use-mock-keychain",  # 用模拟的钥匙串（不会持久化保存，因此不会对系统的实际钥匙串产生任何影响）
    "about:blank",  # 显示一个空白页面
]  # 浏览器默认启动参数

TIMEOUT: int = 30  # 全局的超时时间（s）
LOGGER_LEVEL: int = logging.WARNING  # 日志输出级别
USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"  # 默认 ua
USER_DATA_DIR: str = f"./EasyPageTemp/user_data_"  # 默认用户文件夹（拼接的时候会加上 port）
