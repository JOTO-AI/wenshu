# 🚀 智能问数系统快速启动指南

## 本地开发环境启动

### 前置要求

- Node.js 20+
- Python 3.11+
- pnpm
- uv (Python 包管理器)

### 启动步骤

1. **配置开发环境**:

   为确保端口稳定性，在项目根目录创建 `.env.development` 文件：

   ```bash
   # 创建开发环境配置
   cat > .env.development << 'EOF'
   # 前端应用端口 - 固定为3001避免端口冲突
   WEB_APP_PORT=3001
   # API端口
   API_PORT=8000
   # CORS配置
   CORS_ORIGINS=http://localhost:3001,http://localhost:3000,http://localhost:4200
   EOF
   ```

2. **安装依赖**:

   ```bash
   # 安装前端依赖
   pnpm install

   # 进入API目录安装后端依赖
   cd apps/api
   uv sync
   cd ../..
   ```

3. **启动开发服务**:

   ```bash
   # 启动所有服务
   pnpm run dev

        # 或分别启动
     pnpm run dev:web    # 前端 (端口: 3001)
     pnpm run dev:api    # 后端 (端口: 8000)
   ```

4. **访问应用**:
   - 前端: http://localhost:3001
   - 后端 API: http://localhost:8000
   - API 文档: http://localhost:8000/docs

### 端口配置说明

| 服务            | 端口 | 说明                   |
| --------------- | ---- | ---------------------- |
| 前端开发服务器  | 3001 | 固定端口，避免自动分配 |
| 后端 API 服务器 | 8000 | FastAPI 开发服务器     |
| HMR 热更新      | 4001 | 前端端口+1000          |

**端口稳定性**：

- `vite.config.ts` 中设置了 `strictPort: true`
- 如果 3001 端口被占用，服务会报错而不是自动切换端口
- 这确保了开发环境的一致性

### 开发环境故障排查

#### 端口被占用

```bash
Error: Port 3001 is already in use
```

**解决方案**：

```bash
# 查找占用端口的进程
lsof -i :3001
# 终止占用进程（替换<PID>为实际进程ID）
kill -9 <PID>
# 或修改端口
echo "WEB_APP_PORT=3002" >> .env.development
```

#### CORS 错误

确保后端 API 的 CORS_ORIGINS 包含前端地址：

```bash
# 在 .env.development 中设置
CORS_ORIGINS=http://localhost:3001,http://localhost:3000,http://localhost:4200
```

## Docker 环境启动

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+

### 启动步骤

1. **配置环境变量**:

   ```bash
   cp docker.env.example .env
   # 根据需要编辑 .env 文件
   ```

2. **构建并启动**:

   ```bash
   # 启动所有服务
   docker compose up -d

   # 查看日志
   docker compose logs -f
   ```

3. **访问应用**:

   - 前端: http://localhost:80
   - 后端 API: http://localhost:8000
   - API 文档: http://localhost:8000/docs

4. **停止服务**:
   ```bash
   docker compose down
   ```

## 内网部署

### GitHub Actions 自动部署

1. **配置 Secrets** (在 GitHub 仓库设置中):

   ```
   VPN_SERVER=your-vpn-server.com
   VPN_USERNAME=your-username
   VPN_PASSWORD=your-password
   VPN_SERVER_CERT=pin-sha256:your-server-certificate-fingerprint
   DEPLOY_HOST=your-internal-server-ip
   DEPLOY_USER=deploy
   DEPLOY_PASSWORD=your-server-password
   DEPLOY_PATH=~/wenshu
   ```

   **证书指纹配置**：

   ```bash
   # 根据您本地连接VPN时的输出，使用以下指纹：
   VPN_SERVER_CERT=xxx
   # 注意：本地电脑和GitHub Actions必须使用完全相同的指纹
   ```

2. **触发部署**:
   - 推送到 `main` 分支自动部署到 staging
   - 手动触发选择环境部署

### 手动内网部署

1. **在目标服务器上**:

   ```bash
   # 克隆代码
   git clone <repository-url>
   cd wenshu

   # 配置环境
   cp docker.env.example .env
   # 编辑 .env 文件

   # 执行部署
   ./scripts/deploy.sh staging
   ```

## 常用命令

### 开发命令

```bash
# 代码格式化
pnpm run format

# 代码检查
pnpm run lint

# 类型检查
pnpm run typecheck

# 运行测试
pnpm run test

# 构建项目
pnpm run build
```

### Docker 命令

```bash
# 查看容器状态
docker compose ps

# 查看日志
docker compose logs -f [service-name]

# 重启服务
docker compose restart [service-name]

# 清理未使用资源
docker system prune -f
```

### 部署命令

```bash
# 部署到staging环境
./scripts/deploy.sh staging

# 部署到production环境
./scripts/deploy.sh production

# 查看部署状态
docker compose ps
```

## 健康检查

### API 健康检查

```bash
curl http://localhost:8000/health
```

### Web 健康检查

```bash
curl http://localhost:80/health
```

## 故障排查

### 端口冲突

```bash
# 查看端口占用
netstat -tulpn | grep 8000
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

### 容器问题

```bash
# 查看容器日志
docker logs <container-name>

# 进入容器调试
docker exec -it <container-name> /bin/bash
```

### VPN 连接问题

```bash
# 测试VPN服务器连通性
ping <vpn-server>

# 检查OpenConnect安装
which openconnect
openconnect --version
```

## 获取帮助

- 查看详细部署文档: `DEPLOYMENT.md`
- 查看项目架构: `docs/`
- 技术支持: [联系信息]

---

_快速启动指南 - 最后更新: $(date +%Y-%m-%d)_
