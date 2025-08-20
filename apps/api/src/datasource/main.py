from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import async_engine
from app.core.casbin import casbin_service
from app.api import router as api_router
from app.models import Base
from app.services import PermissionService, UserService, RoleService
from app.core.database import get_async_session
from app.core.security import get_password_hash


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("正在启动数据源管理系统...")
    
    # 创建数据库表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 初始化数据
    await init_data()
    
    logger.info("数据源管理系统启动完成")
    
    yield
    
    # 关闭时执行
    logger.info("正在关闭数据源管理系统...")
    await async_engine.dispose()
    logger.info("数据源管理系统已关闭")


async def init_data():
    """初始化数据"""
    try:
        async for db in get_async_session():
            # 初始化权限
            permission_service = PermissionService(db)
            await permission_service.init_default_permissions()
            
            # 创建默认管理员用户
            user_service = UserService(db)
            admin_user = await user_service.get_user_by_email(settings.admin_email)
            
            if not admin_user:
                from app.schemas import UserCreate
                admin_data = UserCreate(
                    username="admin",
                    email=settings.admin_email,
                    password=settings.admin_password,
                    full_name="系统管理员",
                    is_superuser=True,
                    is_verified=True
                )
                admin_user = await user_service.create_user(admin_data)
                logger.info(f"创建了默认管理员用户: {settings.admin_email}")
            
            # 创建默认角色
            role_service = RoleService(db)
            admin_role = await role_service.get_role_by_name("admin")
            
            if not admin_role:
                from app.schemas import RoleCreate
                admin_role_data = RoleCreate(
                    name="admin",
                    description="超级管理员角色",
                    permission_ids=[]
                )
                admin_role = await role_service.create_role(admin_role_data)
                logger.info("创建了默认管理员角色")
            
            # 为管理员分配角色
            if admin_role not in admin_user.roles:
                await user_service.assign_roles(admin_user.id, [admin_role.id])
                logger.info("为管理员用户分配了角色")
            
            break
            
    except Exception as e:
        logger.error(f"初始化数据失败: {e}")


# 创建FastAPI应用
app = FastAPI(
    title="数据源管理系统",
    description="基于FastAPI的数据源管理后端系统，支持RBAC权限控制",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理的异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "服务器内部错误",
            "status_code": 500
        }
    )


# 健康检查
@app.get("/health", tags=["系统"])
async def health_check():
    """健康检查接口"""
    return {
        "success": True,
        "message": "服务正常运行",
        "version": "1.0.0"
    }


# 包含API路由
app.include_router(api_router, prefix="/admin")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        # reload=settings.debug,
        log_level="info"
    )
