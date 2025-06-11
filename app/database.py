import aiomysql
from contextlib import asynccontextmanager
import os
from typing import Dict, List, Union, Optional
from .logger import LoggerFactory

# 初始化日志记录器
logger = LoggerFactory.get_logger("database")


class MySQLConnection:
    """
    MySQL 数据库连接管理器
    """

    _pool = None

    @classmethod
    async def create_pool(cls):
        """创建数据库连接池"""
        if cls._pool is None:
            try:
                cls._pool = await aiomysql.create_pool(
                    host=os.getenv("MYSQL_HOST", "db"),
                    port=int(os.getenv("MYSQL_PORT", 3306)),
                    user=os.getenv("MYSQL_USER", "root"),
                    password=os.getenv("MYSQL_PASSWORD", "securepass"),
                    db=os.getenv("MYSQL_DATABASE", "appdb"),
                    minsize=5,
                    maxsize=20,
                    autocommit=True,
                    connect_timeout=5,
                )
                logger.info("Database connection pool created")
            except Exception as e:
                logger.error(f"Failed to create database pool: {str(e)}")
                raise
        return cls._pool

    @classmethod
    async def close_pool(cls):
        """关闭数据库连接池"""
        if cls._pool:
            cls._pool.close()
            await cls._pool.wait_closed()
            logger.info("Database connection pool closed")
            cls._pool = None

    @classmethod
    @asynccontextmanager
    async def get_connection(cls):
        """获取数据库连接（上下文管理器）"""
        if cls._pool is None:
            await cls.create_pool()

        conn = await cls._pool.acquire()
        try:
            yield conn
        finally:
            cls._pool.release(conn)

    @classmethod
    async def execute_query(
        cls, sql: str, parameters: Optional[Dict] = None
    ) -> Dict[str, Union[int, List[Dict]]]:
        """
        执行 SQL 查询并返回结果

        :param sql: SQL 语句
        :param parameters: SQL 参数
        :return: 包含结果的字典
        """
        parameters = parameters or {}
        result = {"rowcount": 0, "rows": []}

        # 将字典参数转换为元组
        param_tuple = tuple(parameters.values())

        async with cls.get_connection() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    # 执行参数化查询
                    await cursor.execute(sql, param_tuple)

                    # 处理 SELECT 查询
                    if cursor.description:
                        rows = await cursor.fetchall()
                        result["rows"] = rows
                        result["rowcount"] = len(rows)

                    # 处理 INSERT/UPDATE/DELETE
                    else:
                        result["rowcount"] = cursor.rowcount

                except aiomysql.Error as e:
                    error_code = e.args[0]
                    error_message = e.args[1]

                    # 分类错误类型
                    if error_code in (1045, 1044, 1049):  # 认证/数据库错误
                        logger.error(f"数据库连接错误: {error_message}")
                        raise DatabaseError(
                            f"数据库连接错误: {error_code}", "db_access"
                        )
                    elif error_code in (1054, 1064, 1146):  # SQL 语法错误
                        logger.warning(f"SQL语法错误: {error_message}")
                        raise DatabaseError(f"SQL语法错误: {error_code}", "sql_syntax")
                    elif error_code in (1213, 1205):  # 死锁/锁超时
                        logger.warning(f"数据库锁异常: {error_message}")
                        raise DatabaseError(f"数据库锁异常: {error_code}", "db_lock")
                    else:  # 其他数据库错误
                        logger.error(f"其他数据库错误 [{error_code}]: {error_message}")
                        raise DatabaseError(
                            f"其他数据库错误: {error_code}", "db_general"
                        )

                except Exception as e:
                    logger.exception("sql执行时程序异常")
                    raise DatabaseError("sql执行时程序异常", "db_internal")

        return result

    @classmethod
    async def check_connection(cls) -> bool:
        """检查数据库连接是否正常"""
        try:
            async with cls.get_connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT 1")
                    result = await cursor.fetchone()
                    return result[0] == 1
        except Exception:
            return False


class DatabaseError(Exception):
    """自定义数据库异常"""

    def __init__(self, message: str, error_type: str):
        super().__init__(message)
        self.error_type = error_type
        self.message = message

    def to_dict(self) -> Dict[str, str]:
        return {"error_type": self.error_type, "message": self.message}
