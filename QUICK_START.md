# 🚀 智能问数系统快速启动指南

## 本地开发环境启动

### 前置要求

- Node.js 20+
- Python 3.11+
- pnpm
- uv (Python 包管理器)

### 启动步骤

1. **安装依赖**:

   ```bash
   # 安装前端依赖
   pnpm install

   # 进入API目录安装后端依赖
   cd apps/api
   uv sync
   cd ../..
   ```

2. **启动开发服务**:

   ```bash
   # 启动所有服务
   pnpm run dev

        # 或分别启动
     pnpm run dev:web    # 前端 (端口: 3001)
     pnpm run dev:api    # 后端 (端口: 8000)
   ```

3. **访问应用**:
   - 前端: http://localhost:3001
   - 后端 API: http://localhost:8000
   - API 文档: http://localhost:8000/docs

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
   DEPLOY_HOST=your-internal-server-ip
   DEPLOY_USER=deploy
   DEPLOY_PASSWORD=your-server-password
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
