# 智能问数系统内网部署指南

## 📋 部署概述

本系统支持通过 GitHub Actions 自动部署到公司内网环境，使用 OpenConnect VPN 连接内网，并通过 Docker 容器化部署。

## 🏗️ 架构组件

- **前端**: React 应用 (端口: 80)
- **后端**: FastAPI 应用 (端口: 8000)
- **反向代理**: Nginx (端口: 8080, 生产环境可选)
- **VPN 连接**: OpenConnect
- **容器化**: Docker + Docker Compose

## 🚀 自动化部署

### GitHub Actions 配置

需要在 GitHub 仓库设置以下 Secrets:

#### VPN 相关配置

```
VPN_SERVER=your-vpn-server.com
VPN_USERNAME=your-username
VPN_PASSWORD=your-password
```

#### 服务器部署配置

```
DEPLOY_HOST=your-internal-server-ip
DEPLOY_USER=deploy
DEPLOY_PASSWORD=your-server-password
DEPLOY_PATH=/opt/wenshu
```

### 部署流程

1. **触发方式**:

   - 推送到 `main` 分支自动部署到 staging 环境
   - 推送到 `release/*` 分支自动部署
   - 手动触发可选择环境 (staging/production)

2. **部署步骤**:
   - 连接 OpenConnect VPN
   - 构建 Docker 镜像
   - 传输文件到内网服务器
   - 部署容器服务
   - 健康检查
   - 断开 VPN 连接

## 🔧 手动部署

### 前置要求

1. **服务器要求**:

   - Ubuntu 20.04+ 或 CentOS 8+
   - Docker 20.10+
   - Docker Compose 2.0+
   - 至少 4GB RAM
   - 至少 20GB 磁盘空间

2. **网络要求**:
   - 内网服务器可访问
   - 防火墙开放相应端口 (80, 8000, 8080)

### 部署步骤

1. **克隆代码到服务器**:

   ```bash
   git clone <repository-url>
   cd wenshu
   ```

2. **配置环境变量**:

   ```bash
   cp docker.env.example .env
   # 编辑 .env 文件配置参数
   nano .env
   ```

3. **构建并启动服务**:

   ```bash
   # 使用Docker Compose
   docker-compose up -d

   # 或使用部署脚本
   ./scripts/deploy.sh staging
   ```

4. **验证部署**:

   ```bash
   # 检查服务状态
   docker-compose ps

   # 检查健康状态
   curl http://localhost:8000/health
   curl http://localhost:80/health
   ```

## 📊 服务监控

### 健康检查端点

- **API 健康检查**: `GET /health`
- **Web 健康检查**: `GET /health`
- **API 服务状态**: `GET /`

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f api
docker-compose logs -f web
docker-compose logs -f nginx  # 生产环境

# 查看最近日志
docker-compose logs --tail=100 api
```

### 性能监控

```bash
# 查看资源使用情况
docker stats

# 查看容器详情
docker-compose ps
docker inspect <container-name>
```

## 🔐 安全配置

### 环境变量

| 变量名         | 描述           | 示例                                          |
| -------------- | -------------- | --------------------------------------------- |
| `API_PORT`     | API 服务端口   | `8000`                                        |
| `WEB_PORT`     | Web 服务端口   | `80`                                          |
| `PROXY_PORT`   | 代理服务端口   | `8080`                                        |
| `CORS_ORIGINS` | 允许的 CORS 源 | `http://localhost:3001,http://localhost:3000` |
| `LOG_LEVEL`    | 日志级别       | `INFO`                                        |

### 安全特性

- 非 root 用户运行容器
- 安全 HTTP 头设置
- 请求频率限制
- 文件上传大小限制
- CORS 配置
- 隐藏服务器版本信息

## 🛠️ 故障排查

### 常见问题

1. **VPN 连接失败**:

   ```bash
   # 检查VPN服务器连通性
   ping $VPN_SERVER

   # 检查认证信息
   echo $VPN_USERNAME
   ```

2. **容器启动失败**:

   ```bash
   # 查看容器日志
   docker-compose logs <service-name>

   # 检查端口占用
   netstat -tulpn | grep <port>
   ```

3. **服务不可访问**:

   ```bash
   # 检查防火墙
   sudo ufw status

   # 检查服务绑定
   docker-compose ps
   ```

### 回滚操作

```bash
# 停止当前服务
docker-compose down

# 加载备份镜像
docker load < /opt/wenshu/backups/backup_YYYYMMDD_HHMMSS/images.tar.gz

# 启动备份版本
docker-compose up -d
```

## 📈 维护操作

### 清理操作

```bash
# 清理未使用的镜像
docker image prune -f

# 清理未使用的容器
docker container prune -f

# 清理未使用的网络
docker network prune -f

# 清理构建缓存
docker builder prune -f
```

### 备份操作

```bash
# 手动备份
./scripts/deploy.sh staging  # 会自动创建备份

# 查看备份
ls -la /opt/wenshu/backups/
```

### 更新操作

```bash
# 拉取最新代码
git pull origin main

# 重新部署
./scripts/deploy.sh production
```

## 📞 支持联系

- **技术支持**: [技术团队联系方式]
- **紧急联系**: [紧急联系方式]
- **文档地址**: [文档地址]

---

_最后更新: $(date +%Y-%m-%d)_
