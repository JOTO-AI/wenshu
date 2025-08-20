from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.services import AuthService, get_current_user
from app.schemas import UserLogin, LoginResponse, TokenRefresh, Response
from app.models import User


router = APIRouter()


@router.post("/login", response_model=LoginResponse, summary="管理员登录")
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_async_session)
):
    """
    管理员登录接口
    
    - **email**: 用户邮箱
    - **password**: 用户密码
    """
    auth_service = AuthService(db)
    return await auth_service.login(login_data)


@router.post("/refresh", response_model=LoginResponse, summary="刷新Token")
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_async_session)
):
    """
    刷新访问令牌
    
    - **refresh_token**: 刷新令牌
    """
    auth_service = AuthService(db)
    return await auth_service.refresh_token(token_data)


@router.post("/logout", response_model=Response, summary="退出登录")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    退出登录，清除用户的刷新令牌
    """
    auth_service = AuthService(db)
    await auth_service.logout(current_user.id)
    
    return Response(message="退出登录成功")


@router.get("/me", response_model=dict, summary="获取当前用户信息")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户的详细信息
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "phone": current_user.phone,
        "department": current_user.department,
        "position": current_user.position,
        "avatar": current_user.avatar,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
        "roles": [{"id": role.id, "name": role.name, "description": role.description} for role in current_user.roles]
    }
