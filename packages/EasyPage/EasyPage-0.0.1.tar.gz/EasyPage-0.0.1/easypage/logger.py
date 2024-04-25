"""
    日志输出
"""
import logging
from easypage import settings


class Logger:
    def __init__(self, set_level: int = None):
        """

        :param set_level: 设置日志级别（如：logging.DEBUG）
        """
        if not set_level:
            set_level = logging.DEBUG

        # 创建logger对象
        logger = logging.getLogger('EasyPage')

        # 设置日志级别
        logger.setLevel(set_level)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()

        # 设置控制台处理器的日志级别
        console_handler.setLevel(set_level)

        # 创建日志格式器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 将日志格式器添加到处理器
        console_handler.setFormatter(formatter)

        # 将处理器添加到logger
        logger.addHandler(console_handler)

        self.logger = logger

    def debug(self, msg: str, *args):
        if args:
            self.logger.debug(msg.format(*args))
        else:
            self.logger.debug(msg)

    def info(self, msg: str, *args):
        if args:
            self.logger.info(msg.format(*args))
        else:
            self.logger.info(msg)

    def warning(self, msg: str, *args):
        if args:
            self.logger.warning(msg.format(*args))
        else:
            self.logger.warning(msg)

    def error(self, msg: str, *args):
        if args:
            self.logger.error(msg.format(*args))
        else:
            self.logger.error(msg)

    def exception(self, msg: str, *args):
        if args:
            self.logger.exception(msg.format(*args))
        else:
            self.logger.exception(msg)

    def critical(self, msg: str, *args):
        if args:
            self.logger.critical(msg.format(*args))
        else:
            self.logger.critical(msg)


if settings.SYSTEM_TYPE == 'linux':
    logger = Logger()
else:
    from loguru import logger
