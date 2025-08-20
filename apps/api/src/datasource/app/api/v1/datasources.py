from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from app.core.database import get_async_session
from app.services import DatasourceService, get_current_user
from app.schemas import (
    DatasourceCreate, DatasourceUpdate, DatasourceRead, DatasourceTestConnection,
    Response, PaginatedResponse
)
from app.models import User
from app.utils import check_datasource_read, check_datasource_write, check_datasource_delete


router = APIRouter()


# 数据源权限检查包装函数
async def check_datasource_read_permission(
    current_user: User = Depends(get_current_user)
) -> User:
    """检查数据源读取权限的包装函数"""
    return await check_datasource_read(current_user)


async def check_datasource_write_permission(
    current_user: User = Depends(get_current_user)
) -> User:
    """检查数据源写入权限的包装函数"""
    return await check_datasource_write(current_user)


async def check_datasource_delete_permission(
    current_user: User = Depends(get_current_user)
) -> User:
    """检查数据源删除权限的包装函数"""
    return await check_datasource_delete(current_user)


@router.get("", response_model=PaginatedResponse, summary="获取数据源列表")
async def get_datasources(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    datasource_type: Optional[str] = Query(None, description="数据源类型"),    
    is_active: Optional[bool] = Query(None, description="是否活跃"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_read_permission)
):
    """
    获取数据源列表，支持分页和搜索
    """
    datasource_service = DatasourceService(db)
    skip = (page - 1) * size
    
    datasources, total = await datasource_service.get_datasources(
        skip=skip,
        limit=size,
        search=search,        datasource_type=datasource_type,
        is_active=is_active
    )
    
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[DatasourceRead.model_validate(datasource).model_dump() for datasource in datasources],
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.post("", response_model=DatasourceRead, summary="创建数据源")
async def create_datasource(
    datasource_data: DatasourceCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_write_permission)
):
    """
    创建新数据源
    """
    datasource_service = DatasourceService(db)
    datasource = await datasource_service.create_datasource(datasource_data, current_user.id)
    return DatasourceRead.model_validate(datasource)


@router.get("/types", response_model=List[dict], summary="获取数据源类型")
async def get_datasource_types(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_read_permission)
):
    """
    获取支持的数据源类型列表
    """
    datasource_service = DatasourceService(db)
    types = await datasource_service.get_datasource_types()
    return types


@router.get("/statistics", response_model=dict, summary="获取数据源统计")
async def get_datasource_statistics(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_read_permission)
):
    """
    获取数据源统计信息
    """
    datasource_service = DatasourceService(db)
    stats = await datasource_service.get_datasource_statistics()
    return stats


@router.get("/{datasource_id}", response_model=DatasourceRead, summary="获取数据源详情")
async def get_datasource(
    datasource_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_read_permission)
):
    """
    根据数据源ID获取数据源详细信息
    """
    datasource_service = DatasourceService(db)
    datasource = await datasource_service.get_datasource_by_id(datasource_id)
    
    if not datasource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="数据源不存在"
        )
    
    return DatasourceRead.model_validate(datasource)


@router.put("/{datasource_id}", response_model=DatasourceRead, summary="更新数据源")
async def update_datasource(
    datasource_id: int,
    datasource_data: DatasourceUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_write_permission)
):
    """
    更新数据源信息
    """
    datasource_service = DatasourceService(db)
    datasource = await datasource_service.update_datasource(datasource_id, datasource_data)
    return DatasourceRead.model_validate(datasource)


@router.delete("/{datasource_id}", response_model=Response, summary="删除数据源")
async def delete_datasource(
    datasource_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_delete_permission)
):
    """
    删除数据源
    """
    datasource_service = DatasourceService(db)
    await datasource_service.delete_datasource(datasource_id)
    
    return Response(message="数据源删除成功")


@router.post("/{datasource_id}/test", response_model=DatasourceTestConnection, summary="测试连接")
async def test_datasource_connection(
    datasource_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_read_permission)
):
    """
    测试数据源连接
    """
    datasource_service = DatasourceService(db)
    result = await datasource_service.test_connection(datasource_id)
    return result


@router.post("/{datasource_id}/sync", response_model=dict, summary="同步数据源")
async def sync_datasource(
    datasource_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_write_permission)
):
    """
    同步数据源数据
    """
    datasource_service = DatasourceService(db)
    result = await datasource_service.sync_datasource(datasource_id)
    return result


@router.get("/{datasource_id}/schema", response_model=dict, summary="获取数据源结构")
async def get_datasource_schema(
    datasource_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_read_permission)
):
    """
    获取数据源的结构信息（表、字段等）
    """
    datasource_service = DatasourceService(db)
    schema_info = await datasource_service.get_datasource_schema(datasource_id)
    return schema_info


@router.get("/{datasource_id}/tables", response_model=List[str], summary="获取数据源表列表")
async def get_datasource_tables(
    datasource_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_read_permission)
):
    """
    获取数据源的表或集合列表
    """
    datasource_service = DatasourceService(db)
    tables = await datasource_service.get_datasource_tables(datasource_id)
    return tables


@router.post("/{datasource_id}/query", response_model=dict, summary="执行查询")
async def execute_datasource_query(
    datasource_id: int,
    query_data: dict,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_read_permission)
):
    """
    在指定数据源上执行查询
    """
    query = query_data.get("query", "")
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="查询语句不能为空"
        )
    
    datasource_service = DatasourceService(db)
    result = await datasource_service.execute_query(datasource_id, query)
    return result


@router.get("/supported-types", response_model=List[str], summary="获取支持的数据源类型")
async def get_supported_datasource_types(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(check_datasource_read_permission)
):
    """
    获取系统支持的所有数据源类型
    """
    datasource_service = DatasourceService(db)
    types = await datasource_service.get_supported_datasource_types()
    return types
