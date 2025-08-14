#!/bin/bash

# 开发环境管理脚本
# 用于安全启动和停止开发服务，防止僵尸进程

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

# 检查僵尸进程
check_zombie_processes() {
    log_info "检查僵尸进程..."
    
    local nx_processes=$(ps aux | grep -E "nx run-many" | grep -v grep | wc -l)
    local vite_processes=$(ps aux | grep -E "vite.*bin/vite" | grep -v grep | wc -l)
    local uvicorn_processes=$(ps aux | grep -E "uvicorn" | grep -v grep | wc -l)
    
    if [ $nx_processes -gt 0 ]; then
        log_warning "发现 $nx_processes 个 nx run-many 进程"
        ps aux | grep -E "nx run-many" | grep -v grep
    fi
    
    if [ $vite_processes -gt 0 ]; then
        log_warning "发现 $vite_processes 个 vite 进程"
    fi
    
    if [ $uvicorn_processes -gt 0 ]; then
        log_warning "发现 $uvicorn_processes 个 uvicorn 进程"
    fi
    
    return $((nx_processes + vite_processes + uvicorn_processes))
}

# 清理僵尸进程
cleanup_processes() {
    log_info "清理僵尸进程..."
    
    # 停止 nx run-many 进程
    pkill -f "nx run-many" 2>/dev/null || true
    
    # 停止 vite 进程
    pkill -f "vite.*bin/vite" 2>/dev/null || true
    
    # 停止 uvicorn 进程
    pkill -f "uvicorn" 2>/dev/null || true
    
    # 等待进程终止
    sleep 2
    
    # 强制终止顽固进程
    pkill -9 -f "nx run-many" 2>/dev/null || true
    pkill -9 -f "vite.*bin/vite" 2>/dev/null || true
    pkill -9 -f "uvicorn" 2>/dev/null || true
    
    log_success "进程清理完成"
}

# 重置 Nx 环境
reset_nx() {
    log_info "重置 Nx 环境..."
    pnpm nx reset
    log_success "Nx 环境重置完成"
}

# 启动开发环境
start_dev() {
    log_info "启动开发环境..."
    
    # 检查并清理僵尸进程
    if ! check_zombie_processes; then
        log_warning "发现僵尸进程，正在清理..."
        cleanup_processes
        reset_nx
    fi
    
    log_info "使用 pnpm dev 启动所有服务..."
    exec pnpm dev
}

# 启动开发环境（concurrently 方式）
start_dev_all() {
    log_info "启动开发环境 (concurrently)..."
    
    # 检查并清理僵尸进程
    if ! check_zombie_processes; then
        log_warning "发现僵尸进程，正在清理..."
        cleanup_processes
    fi
    
    log_info "使用 pnpm dev:all 启动所有服务..."
    exec pnpm dev:all
}

# 停止开发环境
stop_dev() {
    log_info "停止开发环境..."
    cleanup_processes
    log_success "开发环境已停止"
}

# 显示帮助信息
show_help() {
    echo "开发环境管理脚本"
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  start       启动开发环境 (使用 nx)"
    echo "  start-all   启动开发环境 (使用 concurrently)"
    echo "  stop        停止开发环境"
    echo "  cleanup     清理僵尸进程"
    echo "  check       检查进程状态"
    echo "  reset       重置 Nx 环境"
    echo "  help        显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 start     # 启动开发环境"
    echo "  $0 stop      # 停止开发环境"
    echo "  $0 cleanup   # 清理僵尸进程"
}

# 主函数
main() {
    case "${1:-help}" in
        "start")
            start_dev
            ;;
        "start-all")
            start_dev_all
            ;;
        "stop")
            stop_dev
            ;;
        "cleanup")
            cleanup_processes
            ;;
        "check")
            check_zombie_processes
            if [ $? -eq 0 ]; then
                log_success "没有发现僵尸进程"
            fi
            ;;
        "reset")
            reset_nx
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# 执行主函数
main "$@"
