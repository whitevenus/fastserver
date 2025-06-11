import logging
import os
from typing import Optional


class LoggerFactory:
    _loggers = {}

    @staticmethod
    def get_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
        """
        获取或创建一个日志记录器

        :param name: 日志记录器名称
        :param log_file: 日志文件路径（可选）
        :return: Logger实例
        """
        if name in LoggerFactory._loggers:
            return LoggerFactory._loggers[name]

        # 创建日志记录器
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # 创建格式化器
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 如果指定了日志文件，添加文件处理器
        if log_file:
            # 确保日志目录存在
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        LoggerFactory._loggers[name] = logger
        return logger


# 创建默认日志记录器
logger = LoggerFactory.get_logger("mysql-api", "../logs/mysql_api.log")
