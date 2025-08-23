#!/bin/bash

# 智能问数系统内网部署脚本
# 使用方法: ./deploy.sh [staging|production]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 获取环境参数
ENVIRONMENT=${1:-staging}
DEPLOY_PATH=${DEPLOY_PATH:-/opt/wenshu}
BACKUP_DIR=${BACKUP_DIR:-/opt/wenshu/backups}

log_info "开始部署到 $ENVIRONMENT 环境"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    log_error "Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建必要的目录
log_info "创建部署目录..."
sudo mkdir -p "$DEPLOY_PATH"
sudo mkdir -p "$BACKUP_DIR"

# 进入部署目录
cd "$DEPLOY_PATH"

# 备份当前版本（如果存在）
if [ -f docker-compose.yml ] && docker-compose ps | grep -q "Up"; then
    log_info "备份当前运行的服务..."
    BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR/$BACKUP_NAME"

    # 导出当前镜像
    docker save $(docker-compose config --services | xargs -I {} echo "wenshu-{}:latest") | gzip > "$BACKUP_DIR/$BACKUP_NAME/images.tar.gz"

    # 备份配置文件
    cp docker-compose.yml .env "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true

    log_success "备份完成: $BACKUP_DIR/$BACKUP_NAME"
fi

# 设置环境变量文件
if [ ! -f .env ]; then
    log_info "创建环境配置文件..."
    cp docker.env.example .env
    log_warning "请编辑 .env 文件配置适合您环境的参数"
fi

# 加载Docker镜像（如果存在tar.gz文件）
if [ -f wenshu-api.tar.gz ]; then
    log_info "加载API镜像..."
    docker load < wenshu-api.tar.gz
fi

if [ -f wenshu-web.tar.gz ]; then
    log_info "加载Web镜像..."
    docker load < wenshu-web.tar.gz
fi

# 停止现有服务
if docker-compose ps | grep -q "Up"; then
    log_info "停止现有服务..."
    docker-compose down --remove-orphans
fi

# 启动服务
log_info "启动服务..."
docker-compose up -d

# 等待服务启动
log_info "等待服务启动..."
sleep 30

# 健康检查
log_info "执行健康检查..."

# 检查API服务
API_PORT=$(grep API_PORT .env | cut -d'=' -f2 || echo "8000")
if curl -f http://localhost:${API_PORT}/health > /dev/null 2>&1; then
    log_success "API服务健康检查通过"
else
    log_error "API服务健康检查失败"
    docker-compose logs api
    exit 1
fi

# 检查Web服务
WEB_PORT=$(grep WEB_PORT .env | cut -d'=' -f2 || echo "80")
if curl -f http://localhost:${WEB_PORT}/health > /dev/null 2>&1; then
    log_success "Web服务健康检查通过"
else
    log_error "Web服务健康检查失败"
    docker-compose logs web
    exit 1
fi

# 显示服务状态
log_info "服务状态:"
docker-compose ps

# 显示服务访问地址
log_success "部署完成！"
log_info "服务访问地址:"
log_info "  - API: http://localhost:${API_PORT}"
log_info "  - Web: http://localhost:${WEB_PORT}"
log_info "  - Health API: http://localhost:${API_PORT}/health"
log_info "  - Health Web: http://localhost:${WEB_PORT}/health"

# 清理旧镜像和容器
log_info "清理旧资源..."
docker image prune -f
docker container prune -f

# 清理旧备份（保留最新5个）
if [ -d "$BACKUP_DIR" ]; then
    log_info "清理旧备份（保留最新5个）..."
    ls -1t "$BACKUP_DIR" | tail -n +6 | xargs -I {} rm -rf "$BACKUP_DIR/{}"
fi

log_success "部署脚本执行完成！"

# 显示日志命令提示
log_info "查看日志命令:"
log_info "  - 查看所有服务日志: docker-compose logs -f"
log_info "  - 查看API日志: docker-compose logs -f api"
log_info "  - 查看Web日志: docker-compose logs -f web"
