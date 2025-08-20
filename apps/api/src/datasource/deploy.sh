#!/bin/bash

# 数据源管理系统部署脚本

set -e

echo "🚀 开始部署数据源管理系统..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi


# 停止现有服务
echo "🛑 停止现有服务..."
cd docker
docker-compose down

# 构建镜像
echo "🔨 构建应用镜像..."
docker-compose build

# 启动数据库服务
echo "🗄️ 启动数据库服务..."
docker-compose up -d postgres redis

# 等待数据库启动
echo "⏳ 等待数据库启动..."
sleep 10

# 运行数据库迁移
echo "📊 运行数据库迁移..."
docker-compose run --rm app alembic upgrade head

# 启动所有服务
echo "🌟 启动所有服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 15

# 健康检查
echo "🔍 进行健康检查..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ 部署成功！"
    echo "📖 API文档: http://localhost/docs"
    echo "🔄 ReDoc文档: http://localhost/redoc"
    echo "🔍 健康检查: http://localhost/health"
else
    echo "❌ 健康检查失败，请检查日志"
    docker-compose logs
    exit 1
fi

echo "🎉 数据源管理系统部署完成！"
