@echo off
REM 数据源管理系统部署脚本 (Windows)

echo 🚀 开始部署数据源管理系统...

REM 检查Docker是否安装
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker 未安装，请先安装 Docker
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose 未安装，请先安装 Docker Compose
    exit /b 1
)

REM 停止现有服务
echo 🛑 停止现有服务...
docker-compose down

REM 构建镜像
echo 🔨 构建应用镜像...
docker-compose build

REM 启动数据库服务
echo 🗄️ 启动数据库服务...
docker-compose up -d postgres redis

REM 等待数据库启动
echo ⏳ 等待数据库启动...
timeout /t 10 /nobreak >nul

REM 运行数据库迁移
echo 📊 运行数据库迁移...
docker-compose run --rm app alembic upgrade head

REM 启动所有服务
echo 🌟 启动所有服务...
docker-compose up -d

REM 等待服务启动
echo ⏳ 等待服务启动...
timeout /t 15 /nobreak >nul

REM 健康检查
echo 🔍 进行健康检查...
curl -f http://localhost/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 部署成功！
    echo 📖 API文档: http://localhost/docs
    echo 🔄 ReDoc文档: http://localhost/redoc
    echo 🔍 健康检查: http://localhost/health
) else (
    echo ❌ 健康检查失败，请检查日志
    docker-compose logs
    exit /b 1
)

echo 🎉 数据源管理系统部署完成！
pause
