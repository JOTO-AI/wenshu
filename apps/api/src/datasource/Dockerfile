FROM harbor.jototech.cn/public/python:3.12-slim


# 彻底清理所有现有的源配置
RUN rm -rf /etc/apt/sources.list.d/* && \
    rm -f /etc/apt/sources.list

# 使用阿里云镜像源（完整覆盖）
RUN echo 'deb http://mirrors.aliyun.com/debian/ bookworm main contrib non-free\n\
deb http://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free\n\
deb http://mirrors.aliyun.com/debian/ bookworm-backports main contrib non-free\n\
deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free' > /etc/apt/sources.list



RUN apt-get update && apt-get install build-essential pkg-config vim python3-dev -y
WORKDIR /usr/src/app


# Copy requirements and .env file
COPY requirements.txt ./
COPY docker/.env ./docker/.env
RUN pip install uv -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple && uv pip install --system --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# Copy all source files
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
