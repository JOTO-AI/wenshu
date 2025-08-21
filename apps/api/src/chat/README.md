# Chat 模块 - 智能问数聊天功能

## 概述

Chat 模块是智能问数系统的核心组件，负责处理自然语言对话、Dify 服务集成、会话管理和用户反馈。该模块采用现代化的软件架构设计，具有高可维护性、可测试性和可扩展性。

## 架构设计

### 分层架构

```
├── API Layer (router.py)              # API路由层
├── Business Logic Layer (service.py)  # 业务逻辑层
├── External Service Layer (chat_service.py) # Dify服务集成层
├── Data Layer (models.py)              # 数据模型层
├── Schema Layer (schemas.py)           # 数据验证层
├── Exception Handling (exceptions.py)  # 异常处理层
└── Utilities (utils.py)               # 工具函数层
```

### 核心组件

#### 1. DifyService (chat_service.py) - Dify API集成层
- **send_message**: 发送消息到Dify API
- **submit_feedback**: 提交用户反馈
- **get_messages**: 获取历史消息
- **get_suggested_questions**: 获取建议问题

#### 2. ChatService (service.py) - 业务逻辑协调层
- **process_query**: 处理智能问数查询
- **process_analysis**: 处理数据分析查询
- **get_history**: 获取对话历史
- **submit_feedback**: 处理用户反馈
- **get_suggested_questions**: 获取建议问题

#### 3. 数据模型层
- **ChatSession**: 会话管理模型
- **QueryHistory**: 查询历史模型
- **Feedback**: 用户反馈模型
- **ApiUsage**: API使用统计模型

## 功能特性

### 已实现功能

1. **智能对话管理**

   - 完整的Dify API集成
   - 支持流式和非流式响应
   - 异步请求处理和连接池管理
   - 自动重试和错误恢复机制

2. **多模式查询支持**

   - 智能问数查询（/chat/query）
   - 数据分析查询（/chat/analyze）
   - 支持多种输入格式和文件上传

3. **完整的用户反馈系统**

   - 基于Dify API的反馈机制
   - 支持点赞/点踩/撤销操作
   - 反馈内容记录和管理

4. **智能历史管理**

   - 基于Dify的消息历史获取
   - 支持分页和过滤
   - 会话级别的历史记录

5. **建议问题生成**

   - 动态建议问题推荐
   - 基于上下文的智能推荐
   - 实时问题生成

6. **完善的错误处理**

   - 分层异常处理体系
   - 详细的错误日志记录
   - 用户友好的错误响应

7. **高性能架构**

   - 异步I/O处理
   - HTTP连接池管理
   - 请求重试和超时控制
   - 资源自动清理


## API 文档

### 核心端点

#### 1. 智能问数查询

```http
POST /api/v1/chat/query
```

**请求示例:**

```json
{
    "query": "销售数据的趋势",
    "conversation_id": "optional-conversation-id",
    "inputs": {},
    "stream": false,
    "user": "user-id"
}
```

**响应示例:**

```json
{
    "success": true,
    "conversation_id": "uuid-here",
    "answer": "下面是数据...",
    "message_id": "message-uuid",
    "metadata": {}
}
```

#### 2. 数据分析查询

```http
POST /api/v1/chat/analyze
```

**请求示例:**

```json
{
    "query": "请分析销售数据的趋势",
    "conversation_id": "optional-conversation-id",
    "inputs": {},
    "stream": false,
    "user": "user-id"
}
```

**响应示例:**

```json
{
    "success": true,
    "conversation_id": "uuid-here",
    "answer": "根据数据分析...",
    "message_id": "message-uuid",
    "metadata": {}
}
```

#### 3. 获取对话历史

```http
GET /api/v1/chat/history?user=user-id&conversation_id=conv-id&limit=20
```

**响应示例:**

```json
{
    "limit": 20,
    "has_more": false,
    "data": [
        {
            "id": "msg-id",
            "conversation_id": "conv-id",
            "query": "用户查询",
            "answer": "AI回答",
            "created_at": 1705569239
        }
    ]
}
```

#### 4. 提交反馈

```http
POST /api/v1/chat/feedback
```

**请求示例:**

```json
{
    "message_id": "msg-id",
    "rating": "like",
    "user": "user-id",
    "content": "反馈内容"
}
```

#### 5. 获取建议问题

```http
GET /api/v1/chat/suggested/{message_id}?user=user-id
```

**响应示例:**

```json
[
    "相关问题1",
    "相关问题2",
    "相关问题3"
]
```

## 配置说明

### 环境变量

```env
# AI 服务配置
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_API_KEY=your-api-key

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost/dbname


# 日志配置
LOG_LEVEL=INFO
```

### 配置文件更新

在 `core/config.py` 中添加了完整的配置项：
- Dify服务配置
- 数据库连接
- 日志设置
- 安全配置

## 开发指南

### 本地开发

1. **安装依赖**
   ```bash
   pip install fastapi uvicorn aiohttp pydantic
   ```

2. **环境配置**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件设置配置
   ```

3. **运行服务**
   ```bash
   uvicorn main:app --reload
   ```

### 测试

运行单元测试：
```bash
pytest src/chat/test_chat.py -v
```

### 扩展开发


## 最佳实践

### 1. 错误处理
- 使用自定义异常类型
- 记录详细的错误日志
- 返回用户友好的错误信息

### 2. 性能优化
- 使用异步操作
- 实现连接池
- 添加缓存机制

## 部署指南

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境配置

1. **数据库**
   - 使用 PostgreSQL
   - 配置连接池
   - 启用读写分离

2. **缓存**
   - 使用 Redis 缓存会话数据
   - 缓存建议问题和常用查询


## 路线图（先不实现）

### v1.1 计划功能
- [ ] 完整的数据库持久化
- [ ] 图表生成功能
- [ ] 高级查询分析
- [ ] 用户会话管理

### v1.2 计划功能
- [ ] 多语言支持
- [ ] 插件系统
- [ ] 高级分析功能
- [ ] 企业级集成
