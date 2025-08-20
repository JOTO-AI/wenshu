from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from app.core.database import get_async_session
from app.services import UserService, get_current_user
from app.schemas import (
    UserCreate, UserUpdate, UserRead, UserResetPassword, 
    Response, PaginatedResponse
)
from app.models import User
from app.utils import check_user_read, check_user_write, check_user_delete


router = APIRouter()


# 权限检查依赖函数
async def check_user_read_permission(current_user: User = Depends(get_current_user)) -> User:
    return await check_user_read(current_user)

async def check_user_write_permission(current_user: User = Depends(get_current_user)) -> User:
    return await check_user_write(current_user)

async def check_user_delete_permission(current_user: User = Depends(get_current_user)) -> User:
    return await check_user_delete(current_user)


@router.get("", response_model=PaginatedResponse, summary="获取用户列表")
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_active: Optional[bool] = Query(None, description="是否活跃"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_user_read_permission)
):
    """
    获取用户列表，支持分页和搜索
    
    - **page**: 页码，从1开始
    - **size**: 每页数量，最大100
    - **search**: 搜索关键词，可搜索用户名、邮箱、姓名
    - **is_active**: 过滤活跃状态
    """
    user_service = UserService(db)
    skip = (page - 1) * size
    
    users, total = await user_service.get_users(        skip=skip,
        limit=size,
        search=search,
        is_active=is_active
    )
    
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[UserRead.model_validate(user).model_dump() for user in users],
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.post("", response_model=UserRead, summary="创建用户")
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_user_write_permission)
):
    """
    创建新用户
    
    - **username**: 用户名，唯一
    - **email**: 邮箱，唯一
    - **password**: 密码，最少6位
    - **full_name**: 姓名（可选）
    - **phone**: 电话（可选）
    - **department**: 部门（可选）
    - **position**: 职位（可选）
    """
    user_service = UserService(db)
    user = await user_service.create_user(user_data)
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead, summary="获取用户详情")
async def get_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_user_read_permission)
):
    """
    根据用户ID获取用户详细信息
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return UserRead.model_validate(user)


@router.put("/{user_id}", response_model=UserRead, summary="更新用户")
async def update_user(
    user_id: uuid.UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_user_write_permission)
):
    """
    更新用户信息
    """
    user_service = UserService(db)
    user = await user_service.update_user(user_id, user_data)
    return UserRead.model_validate(user)


@router.delete("/{user_id}", response_model=Response, summary="删除用户")
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_user_delete_permission)
):
    """
    删除用户（软删除，设置为非活跃状态）
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除自己"
        )
    
    user_service = UserService(db)
    await user_service.delete_user(user_id)
    
    return Response(message="用户删除成功")


@router.put("/{user_id}/status", response_model=UserRead, summary="更新用户状态")
async def update_user_status(
    user_id: uuid.UUID,
    is_active: bool,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_user_write_permission)
):
    """
    更新用户的活跃状态
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能修改自己的状态"
        )
    
    user_service = UserService(db)
    user_update = UserUpdate(is_active=is_active)
    user = await user_service.update_user(user_id, user_update)
    
    return UserRead.model_validate(user)


@router.post("/{user_id}/reset-password", response_model=Response, summary="重置密码")
async def reset_user_password(
    user_id: uuid.UUID,
    password_data: UserResetPassword,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_user_write_permission)
):
    """
    重置用户密码
    """
    user_service = UserService(db)
    await user_service.reset_password(user_id, password_data)
    
    return Response(message="密码重置成功")


@router.put("/{user_id}/roles", response_model=UserRead, summary="分配用户角色")
async def assign_user_roles(
    user_id: uuid.UUID,
    role_ids: List[int],
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_user_write_permission)
):
    """
    为用户分配角色
    """
    user_service = UserService(db)
    user = await user_service.assign_roles(user_id, role_ids)
    
    return UserRead.model_validate(user)
