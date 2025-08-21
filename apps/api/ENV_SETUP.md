# 环境变量配置指南

## 📋 配置说明

### 1. 创建 .env 文件

在 `apps/api/` 目录下创建 `.env` 文件：

```bash
# 从示例文件复制
cp .env.example .env
```

### 2. 必需的配置项

#### 🔑 Dify API 配置 (必需)

```env
# Dify 服务基础 URL
DIFY_BASE_URL=https://dify.jototech.cn/v1

# 主要的 Dify API 密钥 (用于问数功能)
DIFY_API_KEY=app-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 分析功能的 Dify API 密钥 (可选)
DIFY_ANALYSIS_API_KEY=app-yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

**获取 API Key 的方法：**
1. 登录您的 Dify 控制台
2. 选择对应的应用
3. 在「API访问」页面获取 API Key
4. 如果有两个不同的应用(问数和分析)，分别获取两个 API Key

### 3. 可选配置项

#### 🌐 CORS 配置

```env
# 前端域名配置，多个用逗号分隔
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

#### ⚙️ Chat 功能配置

```env
# 最大历史记录数量 (默认: 100)
CHAT_MAX_HISTORY=100

# HTTP 请求超时时间，单位秒 (默认: 30)
CHAT_REQUEST_TIMEOUT=30
```

#### 📊 应用配置

```env
# 应用名称 (默认: "智能问数 API")
APP_NAME=智能问数 API

# 调试模式 (默认: false)
DEBUG=false

# 日志级别 (默认: INFO)
LOG_LEVEL=INFO
```

### 4. 完整的 .env 示例

```env
# 应用配置
APP_NAME=智能问数 API
DEBUG=false
LOG_LEVEL=INFO

# Dify 配置 (必需)
DIFY_BASE_URL=https://dify.jototech.cn/v1
DIFY_API_KEY=app-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DIFY_ANALYSIS_API_KEY=app-yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

# Chat 配置
CHAT_MAX_HISTORY=100
CHAT_REQUEST_TIMEOUT=30

# CORS 配置
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# 数据库 (如果需要)
# DATABASE_URL=postgresql://user:pass@localhost:5432/wenshu_db
```

### 5. 环境变量验证

启动应用时，系统会自动验证配置：

```python
# 检查必需的配置
if not settings.dify_api_key:
    logger.warning("DIFY_API_KEY not configured")
```

### 6. 安全注意事项

⚠️ **重要提醒：**

1. **不要提交 .env 文件到版本控制**
   ```bash
   # 确保 .env 在 .gitignore 中
   echo ".env" >> .gitignore
   ```

2. **API Key 安全**
   - 使用强密码保护 API Key
   - 定期轮换 API Key
   - 不要在日志中输出 API Key

3. **生产环境**
   - 使用环境变量而不是 .env 文件
   - 启用 HTTPS
   - 设置适当的 CORS 域名

### 7. 故障排除

#### 常见问题：

**问题 1**: `Dify service not available`
- 检查 `DIFY_API_KEY` 是否正确设置
- 验证 `DIFY_BASE_URL` 是否可访问

**问题 2**: `CORS error`
- 检查 `CORS_ORIGINS` 是否包含前端域名
- 确保域名格式正确（包含协议）

**问题 3**: `Request timeout`
- 增加 `CHAT_REQUEST_TIMEOUT` 值
- 检查网络连接

### 8. 配置检查命令

```bash
# 启动应用并检查配置
cd apps/api
uv run python -c "from src.core.config import settings; print('Config loaded:', settings.app_name)"
```

### 9. 不同环境的配置

#### 开发环境
```env
DEBUG=true
LOG_LEVEL=DEBUG
DIFY_BASE_URL=https://dify-dev.jototech.cn/v1
```

#### 生产环境
```env
DEBUG=false
LOG_LEVEL=INFO
DIFY_BASE_URL=https://dify.jototech.cn/v1
```

---

**📝 配置完成后，重启应用使配置生效！**
