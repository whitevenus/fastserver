# FastServer - MySQL 查询服务

一个基于 FastAPI 实现的 MySQL 查询 HTTP 服务，提供安全可靠的 SQL 查询接口。

## 主要特性

- 基于 FastAPI 框架开发的 RESTful API
- 支持安全的 SELECT/INSERT/UPDATE/DELETE 查询操作
- 内置 SQL 注入防护和参数化查询
- 完整的错误处理机制
- 健康检查接口
- 详细的日志记录
- Docker 化部署支持

## 技术栈

- Python 3.9+
- FastAPI
- MySQL 8.0
- Docker & Docker Compose
- aiomysql
- uvicorn

## 快速开始

### Docker 部署

1. 克隆项目：

   ```bash
   git clone <repository-url>
   cd fastserver
   ```

2. 配置环境变量：
   复制环境变量示例文件并修改配置(只需要修改密码：保持与 secrets/mysql_root_password.txt 文件中一致就可)：

   ```bash
   cp .env.example .env
   ```

3. 启动服务：

   ```bash
   docker compose up -d
   ```

4. 验证服务：
   ```bash
   curl http://localhost:8000/health
   ```

### 本地开发

1. 创建 Python 虚拟环境：

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # 或
   .venv\Scripts\activate    # Windows
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 启动服务：
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 接口文档

### SQL 查询接口

**POST** `/execute-sql`

请求体示例：

```json
{
  "sql": "SELECT * FROM student WHERE age > %s",
  "parameters": {
    "age": 20
  }
}
```

响应示例：

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "张三",
      "age": 22
    }
  ],
  "message": "查询成功执行，影响 1 行"
}
```

### 健康检查接口

**GET** `/health`

响应示例：

```json
{
  "status": "healthy",
  "database": true,
  "version": "1.0.0"
}
```

## 配置说明

环境变量配置（.env 文件）：

```ini
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=test
ALLOWED_ORIGINS=*
PORT=8000
HOST=0.0.0.0
```

## 安全特性

- SQL 查询验证与过滤
- 参数化查询防注入
- 仅允许基本 DML 操作
- 可配置 CORS 策略
- 数据库连接池管理

## 日志管理

- 应用日志位于 `logs/mysql_api.log`
- 包含请求记录、错误信息和系统状态
- 支持按日期滚动的日志文件

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request
