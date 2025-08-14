# 智能问数 (Wenshu)

企业级私有化对话式数据分析平台

## 项目架构

本项目采用 **React + FastAPI + Nx Monorepo** 架构，实现前后端分离的单体应用。

### 技术栈

**前端**

- React 19 + TypeScript
- Vite (构建工具)
- TailwindCSS (样式框架)
- pnpm (包管理器)

**后端**

- Python FastAPI
- uv (Python 包管理器)
- PostgreSQL (数据库)

**开发工具**

- Nx (Monorepo 管理)
- ESLint + Prettier (代码规范)

## 项目结构

```
wenshu/
├── apps/                    # 应用目录
│   ├── web-app/            # React 用户前端
│   ├── admin-app/          # React 管理后台
│   └── api/                # Python FastAPI 后端
├── libs/                   # 共享库
│   ├── shared-types/       # TypeScript 类型定义
│   └── api-client/         # API 客户端库
├── nx.json                 # Nx 配置
├── package.json            # 前端依赖管理
├── pnpm-workspace.yaml     # pnpm 工作空间配置
└── tsconfig.base.json      # TypeScript 基础配置
```

### 架构特点

- **前后端分离**：前端使用 pnpm + Nx 管理，后端使用 uv 独立管理
- **类型安全**：前后端共享 TypeScript 类型定义
- **代码共享**：通过 Nx 实现跨应用的代码复用
- **AI 友好**：清晰的项目结构便于 AI 工具理解和生成代码

## 开发环境设置

### 前置要求

- Node.js >= 18
- Python >= 3.11
- pnpm >= 8
- uv (Python 包管理器)

### 安装依赖

```bash
# 安装前端依赖
pnpm install

# 安装后端依赖
cd apps/api
uv sync
cd ../..
```

## 开发命令

### 启动开发服务器

```bash
# 启动用户前端 (http://localhost:3000)
pnpm dev:web

# 启动管理后台 (http://localhost:4200)
pnpm dev:admin

# 启动 API 后端 (http://localhost:8000)
pnpm dev:api

# 同时启动所有服务（Nx 并行 dev 目标）
pnpm dev

# 或使用并行进程同时启动三个服务
pnpm dev:all
```

### 其他命令

```bash
# 构建所有项目
pnpm build

# 运行所有测试
pnpm test

# 代码检查
pnpm lint

# 全量类型检查（前端所有 TS 项目 + 后端 mypy 可分步执行）
pnpm typecheck

# 查看项目结构
nx graph
```

## 环境变量

可在工作区根目录创建 `.env` 来配置端口与跨域：

```bash
# 前端端口（默认为 3000 / 4200）
WEB_APP_PORT=3000
ADMIN_APP_PORT=4200

# 后端端口（默认 8000）
API_PORT=8000

# 允许的跨域来源（与 apps/api/src/main.py 一致）
CORS_ORIGINS=http://localhost:3000,http://localhost:4200
```

## API 服务

后端 API 服务提供以下端点：

- `GET /` - 服务状态检查
- `GET /health` - 健康检查

API 文档在开发模式下可通过 http://localhost:8000/docs 访问。

后端已内置 CORS，中默认允许 `http://localhost:3000` 与 `http://localhost:4200`，可通过环境变量 `CORS_ORIGINS` 修改。

## 共享库说明

### @wenshu/shared-types

前后端共享的 TypeScript 类型定义，确保数据结构一致性。

### @wenshu/api-client

统一的 API 客户端库，封装所有后端 API 调用逻辑。

## 参考文档

- 架构设计详见 `docs/智能问数系统架构设计-方案一.md`

## 部署

### Docker 部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### 生产构建

```bash
# 构建前端应用
pnpm build

# 构建后端应用
cd apps/api
uv build
```

## 开发指南

### 添加新功能

1. **前端功能**：在 `apps/web-app` 或 `apps/admin-app` 中开发
2. **后端功能**：在 `apps/api/src` 中添加新的路由和逻辑
3. **共享类型**：在 `libs/shared-types` 中定义新的数据类型
4. **API 客户端**：在 `libs/api-client` 中添加新的 API 调用方法

### 代码规范

- 使用 ESLint 和 Prettier 保持代码风格一致
- 遵循 TypeScript 严格模式
- API 接口使用 RESTful 设计原则
- 组件和函数使用描述性命名

## 项目优化

当前项目结构已经过优化：

- **简化依赖**：根目录只保留核心 Nx 和构建工具
- **精简库结构**：只保留必要的共享库（shared-types, api-client）
- **前后端分离**：使用不同的包管理器和构建工具
- **渐进式开发**：避免过早抽象，支持快速迭代

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

MIT License
