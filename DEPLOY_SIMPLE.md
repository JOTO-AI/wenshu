# 智能问数系统部署指南

## 🚀 快速部署

### 前置准备

1. **GitHub Secrets 配置**:
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

2. **服务器要求**:
- Ubuntu 20.04+ 
- Docker 20.10+
- Docker Compose 2.0+

### 自动部署

推送到 `main` 分支自动部署到 staging 环境。

### 访问地址

部署完成后访问：
- **前端应用**: `http://服务器IP`
- **API文档**: `http://服务器IP:8000/docs` 
- **健康检查**: `http://服务器IP/health`

### 手动部署

```bash
# 1. 在服务器上克隆代码
git clone <repository-url>
cd wenshu

# 2. 配置环境
cp docker.env.example .env
# 编辑 .env 文件

# 3. 运行部署脚本  
./scripts/deploy.sh staging
```

### 故障排查

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 重启服务
docker compose restart
```

### 维护操作

```bash
# 停止服务
docker compose down

# 清理旧镜像
docker image prune -f

# 查看磁盘使用
du -sh ~/wenshu
```

---
*简化版部署指南 - 最后更新: 2025-01-20*