from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_async_session
from app.services import RoleService, get_current_user
from app.schemas import (
    RoleCreate, RoleUpdate, RoleRead, RolePermissionUpdate,
    Response, PaginatedResponse
)
from app.models import User
from app.utils import check_role_read, check_role_write, check_role_delete


router = APIRouter()


# 权限检查依赖函数
async def check_role_read_permission(current_user: User = Depends(get_current_user)) -> User:
    return await check_role_read(current_user)

async def check_role_write_permission(current_user: User = Depends(get_current_user)) -> User:
    return await check_role_write(current_user)

async def check_role_delete_permission(current_user: User = Depends(get_current_user)) -> User:
    return await check_role_delete(current_user)


@router.get("", response_model=PaginatedResponse, summary="获取角色列表")
async def get_roles(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_active: Optional[bool] = Query(None, description="是否活跃"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_role_read_permission)
):
    """
    获取角色列表，支持分页和搜索
    """
    role_service = RoleService(db)
    skip = (page - 1) * size
    
    roles, total = await role_service.get_roles(
        skip=skip,
        limit=size,
        search=search,
        is_active=is_active    )
    
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[RoleRead.model_validate(role).model_dump() for role in roles],
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.post("", response_model=RoleRead, summary="创建角色")
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_role_write_permission)
):
    """
    创建新角色
    """
    role_service = RoleService(db)
    role = await role_service.create_role(role_data)
    return RoleRead.model_validate(role)


@router.get("/{role_id}", response_model=RoleRead, summary="获取角色详情")
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_role_read_permission)
):
    """
    根据角色ID获取角色详细信息
    """
    role_service = RoleService(db)
    role = await role_service.get_role_by_id(role_id)
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    return RoleRead.model_validate(role)


@router.put("/{role_id}", response_model=RoleRead, summary="更新角色")
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_role_write_permission)
):
    """
    更新角色信息
    """
    role_service = RoleService(db)
    role = await role_service.update_role(role_id, role_data)
    return RoleRead.model_validate(role)


@router.delete("/{role_id}", response_model=Response, summary="删除角色")
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_role_delete_permission)
):
    """
    删除角色
    """
    role_service = RoleService(db)
    await role_service.delete_role(role_id)
    
    return Response(message="角色删除成功")


@router.put("/{role_id}/permissions", response_model=RoleRead, summary="更新角色权限")
async def update_role_permissions(
    role_id: int,
    permission_data: RolePermissionUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_role_write_permission)
):
    """
    更新角色的权限配置
    """
    role_service = RoleService(db)
    role = await role_service.assign_permissions(role_id, permission_data.permission_ids)
    
    return RoleRead.model_validate(role)


@router.get("/{role_id}/users", response_model=List[dict], summary="获取角色下的用户")
async def get_role_users(
    role_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_role_read_permission)
):
    """
    获取指定角色下的所有用户
    """
    role_service = RoleService(db)
    users = await role_service.get_role_users(role_id)
    
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active
        } 
        for user in users
    ]
