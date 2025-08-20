from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .roles import router as roles_router
from .permissions import router as permissions_router
from .datasources import router as datasources_router


api_router = APIRouter()

# 认证相关路由
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["认证管理"]
)

# 用户管理路由
api_router.include_router(
    users_router,
    prefix="/users",
    tags=["用户管理"]
)

# 角色管理路由
api_router.include_router(
    roles_router,
    prefix="/roles",
    tags=["角色管理"]
)

# 权限管理路由
api_router.include_router(
    permissions_router,
    prefix="/permissions", 
    tags=["权限管理"]
)

# 数据源管理路由
api_router.include_router(
    datasources_router,
    prefix="/datasources",
    tags=["数据源管理"]
)
