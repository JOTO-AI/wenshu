# 开发环境配置指南

## 环境变量配置

为了确保端口稳定性和一致性，请按以下步骤配置本地开发环境：

### 1. 创建本地环境变量文件

在项目根目录创建 `.env.development` 文件：

```bash
# 复制以下内容到 .env.development 文件
cat > .env.development << 'EOF'
# 开发环境配置
# 前端应用端口 - 固定为3001避免端口冲突
WEB_APP_PORT=3001

# API端口
API_PORT=8000

# CORS配置 - 包含开发环境的前端端口
CORS_ORIGINS=http://localhost:3001,http://localhost:3000,http://localhost:4200
EOF
```

### 2. 端口配置说明

| 服务            | 端口 | 说明                   |
| --------------- | ---- | ---------------------- |
| 前端开发服务器  | 3001 | 固定端口，避免自动分配 |
| 后端 API 服务器 | 8000 | FastAPI 开发服务器     |
| HMR 热更新      | 4001 | 前端端口+1000          |

### 3. 端口稳定性保证

- `vite.config.ts` 中设置了 `strictPort: true`
- 如果 3001 端口被占用，服务会报错而不是自动切换端口
- 这确保了开发环境的一致性

### 4. 常见问题解决

#### 端口被占用错误

```bash
Error: Port 3001 is already in use
```

**解决方案**：

```bash
# 查找占用端口的进程
lsof -i :3001

# 终止占用进程（替换<PID>为实际进程ID）
kill -9 <PID>

# 或者修改环境变量使用其他端口
echo "WEB_APP_PORT=3002" >> .env.development
```

#### 跨域问题

如果遇到 CORS 错误，确保后端 API 的 CORS_ORIGINS 包含前端地址：

```bash
# 在 .env.development 中设置
CORS_ORIGINS=http://localhost:3001,http://localhost:3000,http://localhost:4200
```

### 5. 验证配置

启动开发服务器后，应该看到：

```bash
➜  Local:   http://localhost:3001/
```

如果端口不是 3001，请检查：

1. `.env.development` 文件是否存在
2. `WEB_APP_PORT` 变量是否正确设置
3. 是否有其他进程占用端口

## Docker 环境配置

在 Docker 环境中，端口映射在 `docker-compose.yml` 中配置：

```yaml
web:
  ports:
    - '${WEB_PORT:-80}:80' # Docker内部使用nginx的80端口
api:
  ports:
    - '${API_PORT:-8000}:8000' # API服务端口
```

## 生产环境部署

生产环境端口配置：

- 前端：通过 nginx 代理，默认 80 端口
- 后端：8000 端口
- 代理：8080 端口（可选）

详见 `DEPLOYMENT.md` 文档。
