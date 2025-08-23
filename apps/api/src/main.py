import os
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入功能模块路由
from .auth.router import router as auth_router
from .chat.router import router as chat_router
from .users.router import router as users_router

app = FastAPI(
    title="智能问数 API", description="企业级私有化对话式数据分析平台", version="1.0.0"
)

# 从环境变量获取 CORS 配置
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3001,http://localhost:3000")
allowed_origins = [origin.strip() for origin in cors_origins.split(",")]

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册功能模块路由
app.include_router(auth_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "智能问数 API 服务正在运行", "status": "healthy"}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "wenshu-api"}
