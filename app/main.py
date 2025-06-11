from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from .database import MySQLConnection, DatabaseError
from .security import validate_sql
import os
from dotenv import load_dotenv
from .logger import logger

# 加载环境变量
load_dotenv(".env")


# 定义请求模型
class SQLQuery(BaseModel):
    sql: str = Field(..., description="SQL查询语句")
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="SQL参数")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("应用启动，初始化数据库连接池...")
    await MySQLConnection.create_pool()
    yield
    logger.info("应用关闭，清理数据库连接池...")
    await MySQLConnection.close_pool()


app = FastAPI(
    lifespan=lifespan,
    title="MySQL Query API",
    description="安全的MySQL查询HTTP接口",
    version="1.0.0",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求中间件，用于日志记录
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"收到请求: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"请求处理完成: {response.status_code}")
    return response


@app.post("/execute-sql")
async def execute_sql(query: SQLQuery):
    logger.info(f"执行SQL查询: {query.sql}")

    if not validate_sql(query.sql):
        logger.warning(f"SQL验证失败: {query.sql}")
        raise HTTPException(400, "仅允许 SELECT/INSERT/UPDATE/DELETE 语句")

    try:
        result = await MySQLConnection.execute_query(
            sql=query.sql, parameters=query.parameters
        )
        logger.info(f"SQL执行成功，影响行数: {result['rowcount']}")
        return {
            "status": "success",
            "data": result.get("rows", []),
            "message": f"查询成功执行，影响 {result['rowcount']} 行",
        }
    except DatabaseError as e:
        logger.error(f"数据库错误: {e.error_type} - {e.message}")
        raise HTTPException(
            status_code=500 if e.error_type.startswith("db_") else 400,
            detail=e.to_dict(),
        )
    except Exception as e:
        logger.exception("未预期的错误")
        raise HTTPException(500, "服务器内部错误")


@app.get("/health")
async def health_check():
    logger.info("执行健康检查")
    db_ok = await MySQLConnection.check_connection()
    status = "healthy" if db_ok else "unhealthy"
    logger.info(f"健康检查结果: {status}")
    return {"status": status, "database": db_ok, "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn

    # 确保日志目录存在
    os.makedirs("logs", exist_ok=True)

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"启动服务器于 {host}:{port}")
    uvicorn.run(app, host=host, port=port, timeout_keep_alive=30, log_config=None)
