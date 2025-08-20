from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
import uuid

from app.core.database import get_async_session, get_redis
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.services.user_service import UserService
from app.schemas import UserLogin, LoginResponse, TokenRefresh
from app.models import User


security = HTTPBearer()


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)

    async def login(self, login_data: UserLogin) -> LoginResponse:
        """用户登录"""
        # 验证用户凭据
        user = await self.user_service.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账户已被禁用"
            )
        
        # 生成令牌
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
          # 将刷新令牌存储到Redis
        redis_client = await get_redis()
        expire_seconds = int(timedelta(days=7).total_seconds())
        await redis_client.setex(
            f"refresh_token:{user.id}",
            expire_seconds,
            refresh_token
        )
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user
        )

    async def refresh_token(self, token_data: TokenRefresh) -> LoginResponse:
        """刷新令牌"""
        # 验证刷新令牌
        user_id = verify_token(token_data.refresh_token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的刷新令牌"
            )
        
        # 检查Redis中的刷新令牌
        redis_client = await get_redis()
        stored_token = await redis_client.get(f"refresh_token:{user_id}")
        if not stored_token or stored_token != token_data.refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="刷新令牌已过期或无效"
            )
        
        # 获取用户信息
        user = await self.user_service.get_user_by_id(uuid.UUID(user_id))
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在或已被禁用"
            )
        
        # 生成新的令牌
        access_token = create_access_token(subject=str(user.id))
        new_refresh_token = create_refresh_token(subject=str(user.id))
          # 更新Redis中的刷新令牌
        expire_seconds = int(timedelta(days=7).total_seconds())
        await redis_client.setex(
            f"refresh_token:{user.id}",
            expire_seconds,
            new_refresh_token
        )
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            user=user
        )

    async def logout(self, user_id: uuid.UUID) -> bool:
        """用户登出"""
        # 从Redis中删除刷新令牌
        redis_client = await get_redis()
        await redis_client.delete(f"refresh_token:{user_id}")
        
        return True

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
        """获取当前用户"""
        # 验证访问令牌
        user_id = verify_token(credentials.credentials)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的访问令牌"
            )
        
        # 获取用户信息
        user = await self.user_service.get_user_by_id(uuid.UUID(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账户已被禁用"
            )
        
        return user


# 依赖注入函数
async def get_auth_service(db: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(db)


async def get_current_user(
    auth_service: AuthService = Depends(get_auth_service),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """获取当前用户的依赖注入函数"""
    user_id = verify_token(credentials.credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的访问令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await auth_service.user_service.get_user_by_id(uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账户已被禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃超级用户"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user
