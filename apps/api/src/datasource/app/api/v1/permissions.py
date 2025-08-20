from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_async_session
from app.services import PermissionService, get_current_user
from app.schemas import (
    PermissionCreate, PermissionUpdate, PermissionRead, PermissionTree,
    Response, PaginatedResponse
)
from app.models import User
from app.utils import check_permission_read, check_permission_write


router = APIRouter()


# 权限检查包装函数
async def check_permission_read_permission(
    current_user: User = Depends(get_current_user)
) -> User:
    """检查权限读取权限的包装函数"""
    return await check_permission_read(current_user)


async def check_permission_write_permission(
    current_user: User = Depends(get_current_user)
) -> User:
    """检查权限写入权限的包装函数"""
    return await check_permission_write(current_user)


@router.get("", response_model=PaginatedResponse, summary="获取权限列表")
async def get_permissions(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    resource: Optional[str] = Query(None, description="资源类型"),
    action: Optional[str] = Query(None, description="操作类型"),
    is_active: Optional[bool] = Query(None, description="是否活跃"),
    parent_id: Optional[int] = Query(None, description="父权限ID"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_permission_read_permission)
):
    """
    获取权限列表，支持分页和搜索
    """
    permission_service = PermissionService(db)
    skip = (page - 1) * size
    
    permissions, total = await permission_service.get_permissions(
        skip=skip,
        limit=size,
        search=search,
        resource=resource,        action=action,
        is_active=is_active,
        parent_id=parent_id
    )
    
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[PermissionRead.model_validate(permission).model_dump() for permission in permissions],
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/tree", response_model=List[dict], summary="获取权限树")
async def get_permission_tree(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_permission_read_permission)
):
    """
    获取权限树状结构
    """
    permission_service = PermissionService(db)
    tree = await permission_service.get_permission_tree()
    return tree


@router.post("", response_model=PermissionRead, summary="创建权限")
async def create_permission(
    permission_data: PermissionCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_permission_write_permission)
):
    """
    创建新权限
    """
    permission_service = PermissionService(db)
    permission = await permission_service.create_permission(permission_data)
    return PermissionRead.model_validate(permission)


@router.get("/{permission_id}", response_model=PermissionRead, summary="获取权限详情")
async def get_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_permission_read_permission)
):
    """
    根据权限ID获取权限详细信息
    """
    permission_service = PermissionService(db)
    permission = await permission_service.get_permission_by_id(permission_id)
    
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    return PermissionRead.model_validate(permission)


@router.put("/{permission_id}", response_model=PermissionRead, summary="更新权限")
async def update_permission(
    permission_id: int,
    permission_data: PermissionUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_permission_write_permission)
):
    """
    更新权限信息
    """
    permission_service = PermissionService(db)
    permission = await permission_service.update_permission(permission_id, permission_data)
    return PermissionRead.model_validate(permission)


@router.delete("/{permission_id}", response_model=Response, summary="删除权限")
async def delete_permission(
    permission_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_permission_write_permission)
):
    """
    删除权限
    """
    permission_service = PermissionService(db)
    await permission_service.delete_permission(permission_id)
    
    return Response(message="权限删除成功")


@router.get("/resources/{resource}", response_model=List[PermissionRead], summary="获取资源权限")
async def get_permissions_by_resource(
    resource: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_permission_read_permission)
):
    """
    根据资源获取相关权限
    """
    permission_service = PermissionService(db)
    permissions = await permission_service.get_permissions_by_resource(resource)
    
    return [PermissionRead.model_validate(permission) for permission in permissions]


@router.get("/actions/{action}", response_model=List[PermissionRead], summary="获取操作权限")
async def get_permissions_by_action(
    action: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_permission_read_permission)
):
    """
    根据操作获取相关权限
    """
    permission_service = PermissionService(db)
    permissions = await permission_service.get_permissions_by_action(action)
    
    return [PermissionRead.model_validate(permission) for permission in permissions]
