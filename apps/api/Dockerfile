# 后端API Dockerfile
FROM python:3.11-slim AS builder

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 设置工作目录
WORKDIR /app

# 复制项目配置文件
COPY pyproject.toml .

# 创建虚拟环境并安装依赖
RUN uv venv .venv && \
    uv pip install -r pyproject.toml

# 生产阶段
FROM python:3.11-slim

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app

# 设置工作目录
WORKDIR /app

# 从builder阶段复制虚拟环境
COPY --from=builder /app/.venv /app/.venv

# 将虚拟环境添加到PATH
ENV PATH="/app/.venv/bin:$PATH"

# 复制应用代码
COPY --chown=app:app src ./src

# 切换到非root用户
USER app

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
