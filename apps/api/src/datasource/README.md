# 数据源管理系统 (Datasource Management System)

一个功能完整的企业级数据源管理系统，基于 FastAPI 构建，支持多种数据库类型的统一管理和操作。

## 🚀 主要特性

### 🔐 安全认证与授权

- **JWT 令牌认证**：支持访问令牌和刷新令牌机制
- **基于角色的访问控制 (RBAC)**：使用 Casbin 实现细粒度权限管理
- **用户角色权限管理**：支持多角色分配和权限继承
- **密码加密存储**：数据源密码采用 AES 加密存储

### 📊 多数据源支持

- **PostgreSQL**：全功能支持，包括连接测试、表结构获取、SQL 查询执行
- **MySQL**：完整的数据库操作支持
- **MongoDB**：支持集合操作和 JSON 查询
- **可扩展架构**：通过适配器模式轻松添加新的数据源类型

### 🛠 数据源管理功能

- **连接管理**：创建、更新、删除和测试数据源连接
- **连接状态监控**：实时检测数据源连接状态
- **架构信息获取**：自动获取数据库表结构和字段信息
- **查询执行**：安全的 SQL/NoSQL 查询执行
- **数据同步**：支持数据源元数据同步

### 👥 用户与权限管理

- **用户管理**：完整的用户生命周期管理
- **角色管理**：灵活的角色定义和权限分配
- **权限树结构**：支持层级权限管理
- **超级管理员**：拥有所有权限的特殊用户

### 📈 监控与统计

- **数据源统计**：按类型、状态等维度统计
- **操作日志**：详细的操作审计日志
- **性能监控**：连接响应时间监控

## 🏗 技术架构

### 后端技术栈

- **框架**：FastAPI 0.104.1
- **数据库 ORM**：SQLAlchemy 2.0.23 (异步)
- **数据库迁移**：Alembic 1.12.1
- **缓存**：Redis 5.0.1
- **权限管理**：Casbin 1.22.0
- **认证**：JWT (python-jose)
- **密码哈希**：Passlib + bcrypt
- **异步支持**：asyncio + asyncpg

### 数据库支持

- **PostgreSQL**：主数据库，使用 asyncpg 驱动
- **MySQL**：使用 aiomysql 驱动
- **MongoDB**：使用 motor 驱动

### 项目结构

``` bash
datasource_system/
├── app/
│   ├── api/v1/           # API 路由
│   │   ├── auth.py       # 认证相关
│   │   ├── users.py      # 用户管理
│   │   ├── roles.py      # 角色管理
│   │   ├── permissions.py # 权限管理
│   │   └── datasources.py # 数据源管理
│   ├── core/             # 核心配置
│   │   ├── config.py     # 配置管理
│   │   ├── database.py   # 数据库连接
│   │   ├── security.py   # 安全相关
│   │   └── casbin.py     # 权限控制
│   ├── models/           # 数据模型
│   │   └── models.py     # SQLAlchemy 模型
│   ├── schemas/          # Pydantic 模式
│   │   └── schemas.py    # 请求/响应模式
│   ├── services/         # 业务逻辑
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── role_service.py
│   │   ├── permission_service.py
│   │   └── datasource_service.py
│   ├── adapters/         # 数据源适配器
│   │   └── __init__.py   # 数据库适配器
│   └── utils/            # 工具函数
│       ├── crypto.py     # 加密解密
│       └── permissions.py # 权限装饰器
├── alembic/              # 数据库迁移
├── config/               # 配置文件
│   ├── rbac_model.conf   # Casbin 模型
│   └── rbac_policy.csv   # Casbin 策略
├── tests/                # 测试文件
├── docker-compose.yml    # Docker 部署
├── Dockerfile           # 容器镜像
└── requirements.txt     # 依赖包
```

## 🚀 快速开始

### 环境要求

- Python 3.12+
- PostgreSQL 15+
- Redis 5+
- Docker & Docker Compose (可选)

### 1. 克隆项目

```bash
git clone <repository-url>
cd datasource_system/docker
```

### 2. 环境变量配置

```bash
cp .env.example .env
```


修改 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/datasource_system
DATABASE_URL_SYNC=postgresql://username:password@localhost:5432/datasource_system

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# JWT 配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 管理员账户
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123

# 环境配置
ENVIRONMENT=development
DEBUG=true
```

### 3. 使用 Docker Compose 部署 (推荐)

```bash
# 启动所有服务
docker-compose up -d

# 停止服务
docker-compose down
```

### 4. 手动安装部署

```bash
# 安装依赖
pip install -r requirements.txt

# 数据库迁移
alembic upgrade head

# 初始化数据
python init_db.py

# 启动服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 访问应用

- **API 文档**：<http://localhost:8000/docs>
- **ReDoc 文档**：<http://localhost:8000/redoc>
- **健康检查**：<http://localhost:8000/health>

## 📚 API 文档

### 认证 API

```bash
# 管理员登录
POST /api/v1/auth/login
{
  "email": "admin@example.com",
  "password": "admin123"
}

# 刷新令牌
POST /api/v1/auth/refresh
{
  "refresh_token": "your-refresh-token"
}
```

### 数据源管理 API

```bash
# 创建数据源
POST /api/v1/datasources
{
  "name": "测试PostgreSQL",
  "type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "database": "testdb",
  "username": "testuser",
  "password": "testpass",
  "description": "测试数据源"
}

# 获取数据源列表
GET /api/v1/datasources?page=1&size=20

# 测试连接
POST /api/v1/datasources/{id}/test

# 获取表列表
GET /api/v1/datasources/{id}/tables

# 执行查询
POST /api/v1/datasources/{id}/query
{
  "query": "SELECT * FROM users LIMIT 10"
}
```

### 用户管理 API

```bash
# 创建用户
POST /api/v1/users
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}

# 分配角色
PUT /api/v1/users/{id}/roles
{
  "role_ids": [1, 2]
}
```

## 🔒 权限系统

### 权限模型

系统采用基于资源和操作的权限模型：

- **资源**：users, roles, permissions, datasources
- **操作**：read, write, delete
- **权限示例**：`datasources:read`, `users:write`

### 预设角色

- **super_admin**：系统超级管理员，拥有所有权限
- **admin**：管理员，拥有大部分管理权限
- **user**：普通用户，拥有基本读取权限

### 权限检查

```python
# 使用装饰器检查权限
@require_permission("datasources", "read")
async def get_datasources():
    pass

# 使用依赖注入检查权限
async def endpoint(
    current_user: User = Depends(check_datasource_read_permission)
):
    pass
```

## 🗄 数据源支持

### PostgreSQL

```python
# 连接配置
{
  "type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "database": "mydb",
  "username": "user",
  "password": "pass"
}
```

### MySQL

```python
# 连接配置
{
  "type": "mysql",
  "host": "localhost",
  "port": 3306,
  "database": "mydb",
  "username": "user",
  "password": "pass"
}
```

### MongoDB

```python
# 连接配置
{
  "type": "mongodb",
  "host": "localhost",
  "port": 27017,
  "database": "mydb",
  "username": "user",
  "password": "pass"
}

# 查询示例
{
  "collection": "users",
  "operation": "find",
  "filter": {"status": "active"},
  "limit": 100
}
```

## 🧪 测试

### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-asyncio httpx

# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_datasources.py

# 生成覆盖率报告
pytest --cov=app tests/
```

### 测试数据源

```bash
# 调试认证系统
python debug_auth.py

# 测试数据库连接
python test_db.py
```

## 🐳 Docker 部署

### 构建镜像

```bash
docker build -t datasource-system .

docker run -d \
  -p 8000:8000 \
  --name datasource-container \
  --restart unless-stopped \
  --env-file .env \
  datasource-system
```

### 使用 Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@postgres:5432/db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: datasource_system
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass

  redis:
    image: redis:7-alpine
```

## 🔧 配置说明

### 核心配置

- `DATABASE_URL`: 异步数据库连接字符串
- `DATABASE_URL_SYNC`: 同步数据库连接字符串（用于 Alembic）
- `REDIS_URL`: Redis 连接字符串
- `SECRET_KEY`: JWT 签名密钥

### Casbin 配置

- 模型文件：`config/rbac_model.conf`
- 策略文件：`config/rbac_policy.csv`

### 数据库迁移

```bash
# 创建迁移
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 🚀 生产部署

### 性能优化

- 使用 Gunicorn + Uvicorn 部署
- 配置数据库连接池
- 启用 Redis 缓存
- 配置 Nginx 反向代理

### 安全配置

- 使用强随机 SECRET_KEY
- 配置 HTTPS
- 限制 API 访问频率
- 定期备份数据库

### 监控告警

- 配置应用性能监控 (APM)
- 设置数据库连接监控
- 配置日志聚合和告警

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

## 🆘 常见问题

### Q: 如何添加新的数据源类型？

A: 在 `app/adapters/__init__.py` 中创建新的适配器类，继承 `DatabaseAdapter`，并在 `DatabaseAdapterFactory` 中注册。

### Q: 如何自定义权限？

A: 在 `app/services/permission_service.py` 中添加新权限，并在 Casbin 配置中定义相应策略。

### Q: 数据源密码如何加密？

A: 系统使用 AES 加密算法，密钥从环境变量获取。相关代码在 `app/utils/crypto.py`。

### Q: 如何扩展 API？

A: 在 `app/api/v1/` 目录下添加新的路由文件，并在 `__init__.py` 中注册路由。

---

如有问题或建议，请通过 Issue 反馈或联系开发团队。
