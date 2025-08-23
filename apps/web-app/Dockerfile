# 前端应用 Dockerfile
FROM node:20-alpine as builder

# 安装 pnpm
RUN npm install -g pnpm

# 设置工作目录
WORKDIR /app

# 复制根目录的package.json和pnpm相关文件
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY tsconfig.base.json nx.json ./

# 复制所有workspace配置
COPY libs/ ./libs/
COPY packages/ ./packages/
COPY apps/web-app/ ./apps/web-app/

# 安装依赖
RUN pnpm install --frozen-lockfile

# 构建应用
RUN pnpm exec nx build web-app

# 生产阶段 - 使用nginx提供静态文件
FROM nginx:alpine

# 复制自定义nginx配置
COPY apps/web-app/nginx.conf /etc/nginx/conf.d/default.conf

# 复制构建产物
COPY --from=builder /app/apps/web-app/dist /usr/share/nginx/html

# 创建非root用户
RUN addgroup -g 1001 -S nginx && \
    adduser -S nginx -u 1001

# 修改nginx配置以使用非root用户
RUN sed -i 's/user nginx;/user nginx;/' /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80 || exit 1

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]
