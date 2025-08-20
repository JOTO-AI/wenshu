from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from datetime import datetime
import asyncio
import json
import time
import uuid

from app.models import Datasource, User
from app.schemas import DatasourceCreate, DatasourceUpdate, DatasourceTestConnection
from app.core.security import get_password_hash
from app.utils.crypto import encrypt_password, decrypt_password
from app.adapters import DatabaseAdapterFactory


class DatasourceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_datasource_by_id(self, datasource_id: int) -> Optional[Datasource]:
        """根据ID获取数据源"""
        result = await self.db.execute(
            select(Datasource)
            .options(selectinload(Datasource.creator))
            .where(Datasource.id == datasource_id)
        )
        return result.scalar_one_or_none()

    async def get_datasource_by_name(self, name: str) -> Optional[Datasource]:
        """根据名称获取数据源"""
        result = await self.db.execute(
            select(Datasource).where(Datasource.name == name)
        )
        return result.scalar_one_or_none()

    async def get_datasources(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        datasource_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        creator_id: Optional[uuid.UUID] = None
    ) -> tuple[List[Datasource], int]:
        """获取数据源列表"""
        query = select(Datasource).options(selectinload(Datasource.creator))
        
        # 构建过滤条件
        filters = []
        if search:
            filters.append(
                or_(
                    Datasource.name.ilike(f"%{search}%"),
                    Datasource.description.ilike(f"%{search}%"),
                    Datasource.host.ilike(f"%{search}%")
                )
            )
        if datasource_type:
            filters.append(Datasource.type == datasource_type)
        if is_active is not None:
            filters.append(Datasource.is_active == is_active)
        if creator_id:
            filters.append(Datasource.creator_id == creator_id)
        
        if filters:
            query = query.where(and_(*filters))
        
        # 获取总数
        count_result = await self.db.execute(
            select(Datasource.id).where(and_(*filters)) if filters else select(Datasource.id)
        )
        total = len(count_result.all())
        
        # 获取分页数据
        query = query.offset(skip).limit(limit).order_by(Datasource.created_at.desc())
        result = await self.db.execute(query)
        datasources = result.scalars().all()
        
        return list(datasources), total    
    
    async def create_datasource(self, datasource_data: DatasourceCreate, creator_id: uuid.UUID) -> Datasource:
        """创建数据源"""
        # 检查数据源名是否已存在
        existing_datasource = await self.get_datasource_by_name(datasource_data.name)
        if existing_datasource:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="数据源名已存在"
            )
        
        # 加密密码
        encrypted_password = None
        if datasource_data.password:
            encrypted_password = encrypt_password(datasource_data.password)
        
        # 创建数据源
        datasource = Datasource(
            **datasource_data.model_dump(exclude={"password"}),
            password=encrypted_password,
            creator_id=creator_id
        )
        
        self.db.add(datasource)
        await self.db.commit()
        await self.db.refresh(datasource)
        
        # 重新查询以预加载关系，避免MissingGreenlet错误
        result = await self.db.execute(
            select(Datasource)
            .options(selectinload(Datasource.creator))
            .where(Datasource.id == datasource.id)
        )
        datasource_with_relations = result.scalar_one()
        
        return datasource_with_relations    
    
    async def update_datasource(self, datasource_id: int, datasource_data: DatasourceUpdate) -> Datasource:
        """更新数据源"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        # 检查数据源名是否被其他数据源使用
        if datasource_data.name and datasource_data.name != datasource.name:
            existing_datasource = await self.get_datasource_by_name(datasource_data.name)
            if existing_datasource:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="数据源名已被其他数据源使用"
                )
        
        # 更新数据源信息
        update_data = datasource_data.model_dump(exclude_unset=True)
        
        # 处理密码加密
        if "password" in update_data and update_data["password"]:
            update_data["password"] = encrypt_password(update_data["password"])
        elif "password" in update_data and not update_data["password"]:
            # 如果密码为空，则保持原密码不变
            del update_data["password"]
        
        for field, value in update_data.items():
            setattr(datasource, field, value)
        
        await self.db.commit()
        await self.db.refresh(datasource)
        
        # 重新查询以预加载关系，避免MissingGreenlet错误
        result = await self.db.execute(
            select(Datasource)
            .options(selectinload(Datasource.creator))
            .where(Datasource.id == datasource.id)
        )
        datasource_with_relations = result.scalar_one()
        
        return datasource_with_relations

    async def delete_datasource(self, datasource_id: int) -> bool:
        """删除数据源"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
            await self.db.delete(datasource)
        await self.db.commit()
        
        return True

    async def test_connection(self, datasource_id: int) -> DatasourceTestConnection:
        """测试数据源连接"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        start_time = time.time()
        
        try:
            # 解密密码
            password = None
            if datasource.password:
                password = decrypt_password(datasource.password)
            
            # 创建数据库适配器
            config = {
                "host": datasource.host,
                "port": datasource.port,
                "database": datasource.database,
                "username": datasource.username,
                "password": password,
                "connection_params": json.loads(datasource.connection_params) if datasource.connection_params else {}
            }
            
            adapter = DatabaseAdapterFactory.create_adapter(datasource.type, config)
            success = await adapter.test_connection()
            await adapter.close()
            
            response_time = time.time() - start_time
            
            # 更新连接状态
            datasource.connection_status = "connected" if success else "failed"
            datasource.last_test_at = datetime.utcnow()
            await self.db.commit()
            
            return DatasourceTestConnection(
                success=success,
                message="连接成功" if success else "连接失败",
                response_time=response_time
            )
            
        except Exception as e:
            # 更新连接状态为失败
            datasource.connection_status = "failed"
            datasource.last_test_at = datetime.utcnow()
            await self.db.commit()
            
            return DatasourceTestConnection(
                success=False,
                message=f"连接测试失败: {str(e)}",
                response_time=time.time() - start_time
            )

    async def get_datasource_schema(self, datasource_id: int) -> Dict[str, Any]:
        """获取数据源结构信息"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 解密密码
            password = None
            if datasource.password:
                password = decrypt_password(datasource.password)
            
            # 创建数据库适配器
            config = {
                "host": datasource.host,
                "port": datasource.port,
                "database": datasource.database,
                "username": datasource.username,
                "password": password,
                "connection_params": json.loads(datasource.connection_params) if datasource.connection_params else {}
            }
            
            adapter = DatabaseAdapterFactory.create_adapter(datasource.type, config)
            schema_info = await adapter.get_schema_info()
            await adapter.close()
            
            return schema_info
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"获取数据源结构失败: {str(e)}"
            )

    async def execute_query(self, datasource_id: int, query: str) -> Dict[str, Any]:
        """执行数据源查询"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 解密密码
            password = None
            if datasource.password:
                password = decrypt_password(datasource.password)
            
            # 创建数据库适配器
            config = {
                "host": datasource.host,
                "port": datasource.port,
                "database": datasource.database,
                "username": datasource.username,
                "password": password,
                "connection_params": json.loads(datasource.connection_params) if datasource.connection_params else {}
            }
            
            adapter = DatabaseAdapterFactory.create_adapter(datasource.type, config)
            result = await adapter.execute_query(query)
            await adapter.close()
            
            return result
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"查询执行失败: {str(e)}"
            )

    async def get_datasource_tables(self, datasource_id: int) -> List[str]:
        """获取数据源表/集合列表"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 解密密码
            password = None
            if datasource.password:
                password = decrypt_password(datasource.password)
            
            # 创建数据库适配器
            config = {
                "host": datasource.host,
                "port": datasource.port,
                "database": datasource.database,
                "username": datasource.username,
                "password": password,
                "connection_params": json.loads(datasource.connection_params) if datasource.connection_params else {}
            }
            
            adapter = DatabaseAdapterFactory.create_adapter(datasource.type, config)
            tables = await adapter.get_tables()
            await adapter.close()
            
            return tables
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"获取表列表失败: {str(e)}"
            )

    async def get_supported_datasource_types(self) -> List[str]:
        """获取支持的数据源类型"""
        return DatabaseAdapterFactory.get_supported_types()

    # ...existing code...
    async def sync_datasource(self, datasource_id: int) -> Dict[str, Any]:
        """同步数据源数据"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 这里可以实现具体的数据同步逻辑
            # 比如同步表结构、统计信息等
            
            # 更新同步时间
            datasource.last_sync_at = datetime.utcnow()
            await self.db.commit()
            
            return {
                "success": True,
                "message": "同步成功",
                "sync_time": datasource.last_sync_at
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"同步失败: {str(e)}"
            }

    async def get_datasource_types(self) -> List[Dict[str, str]]:
        """获取支持的数据源类型"""
        return [
            {"value": "postgresql", "label": "PostgreSQL"},
            {"value": "mysql", "label": "MySQL"},
            {"value": "redis", "label": "Redis"},
            {"value": "mongodb", "label": "MongoDB"},
            {"value": "sqlite", "label": "SQLite"},
            {"value": "oracle", "label": "Oracle"},
            {"value": "sqlserver", "label": "SQL Server"},
        ]

    async def get_datasource_statistics(self) -> Dict[str, Any]:
        """获取数据源统计信息"""
        # 总数统计
        total_result = await self.db.execute(select(Datasource.id))
        total = len(total_result.all())
        
        # 活跃数据源统计
        active_result = await self.db.execute(
            select(Datasource.id).where(Datasource.is_active == True)
        )
        active = len(active_result.all())
        
        # 按类型统计
        type_result = await self.db.execute(
            select(Datasource.type).where(Datasource.is_active == True)
        )
        types = [row[0] for row in type_result.all()]
        type_stats = {}
        for db_type in types:
            type_stats[db_type] = type_stats.get(db_type, 0) + 1
        
        # 连接状态统计
        status_result = await self.db.execute(
            select(Datasource.connection_status).where(Datasource.is_active == True)
        )
        statuses = [row[0] for row in status_result.all()]
        status_stats = {}
        for status in statuses:
            status_stats[status] = status_stats.get(status, 0) + 1
        
        return {
            "total": total,
            "active": active,
            "inactive": total - active,
            "by_type": type_stats,
            "by_status": status_stats
        }

    async def get_datasource_schema(self, datasource_id: int) -> Dict[str, Any]:
        """获取数据源结构信息"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 解密密码
            password = None
            if datasource.password:
                password = decrypt_password(datasource.password)
            
            # 创建数据库适配器
            config = {
                "host": datasource.host,
                "port": datasource.port,
                "database": datasource.database,
                "username": datasource.username,
                "password": password,
                "connection_params": json.loads(datasource.connection_params) if datasource.connection_params else {}
            }
            
            adapter = DatabaseAdapterFactory.create_adapter(datasource.type, config)
            schema_info = await adapter.get_schema_info()
            await adapter.close()
            
            return schema_info
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"获取数据源结构失败: {str(e)}"
            )

    async def execute_query(self, datasource_id: int, query: str) -> Dict[str, Any]:
        """执行数据源查询"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 解密密码
            password = None
            if datasource.password:
                password = decrypt_password(datasource.password)
            
            # 创建数据库适配器
            config = {
                "host": datasource.host,
                "port": datasource.port,
                "database": datasource.database,
                "username": datasource.username,
                "password": password,
                "connection_params": json.loads(datasource.connection_params) if datasource.connection_params else {}
            }
            
            adapter = DatabaseAdapterFactory.create_adapter(datasource.type, config)
            result = await adapter.execute_query(query)
            await adapter.close()
            
            return result
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"查询执行失败: {str(e)}"
            )

    async def get_datasource_tables(self, datasource_id: int) -> List[str]:
        """获取数据源表/集合列表"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 解密密码
            password = None
            if datasource.password:
                password = decrypt_password(datasource.password)
            
            # 创建数据库适配器
            config = {
                "host": datasource.host,
                "port": datasource.port,
                "database": datasource.database,
                "username": datasource.username,
                "password": password,
                "connection_params": json.loads(datasource.connection_params) if datasource.connection_params else {}
            }
            
            adapter = DatabaseAdapterFactory.create_adapter(datasource.type, config)
            tables = await adapter.get_tables()
            await adapter.close()
            
            return tables
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"获取表列表失败: {str(e)}"
            )

    async def get_supported_datasource_types(self) -> List[str]:
        """获取支持的数据源类型"""
        return DatabaseAdapterFactory.get_supported_types()

    # ...existing code...
    async def sync_datasource(self, datasource_id: int) -> Dict[str, Any]:
        """同步数据源数据"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 这里可以实现具体的数据同步逻辑
            # 比如同步表结构、统计信息等
            
            # 更新同步时间
            datasource.last_sync_at = datetime.utcnow()
            await self.db.commit()
            
            return {
                "success": True,
                "message": "同步成功",
                "sync_time": datasource.last_sync_at
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"同步失败: {str(e)}"
            }

    async def get_datasource_types(self) -> List[Dict[str, str]]:
        """获取支持的数据源类型"""
        return [
            {"value": "postgresql", "label": "PostgreSQL"},
            {"value": "mysql", "label": "MySQL"},
            {"value": "redis", "label": "Redis"},
            {"value": "mongodb", "label": "MongoDB"},
            {"value": "sqlite", "label": "SQLite"},
            {"value": "oracle", "label": "Oracle"},
            {"value": "sqlserver", "label": "SQL Server"},
        ]

    async def get_datasource_statistics(self) -> Dict[str, Any]:
        """获取数据源统计信息"""
        # 总数统计
        total_result = await self.db.execute(select(Datasource.id))
        total = len(total_result.all())
        
        # 活跃数据源统计
        active_result = await self.db.execute(
            select(Datasource.id).where(Datasource.is_active == True)
        )
        active = len(active_result.all())
        
        # 按类型统计
        type_result = await self.db.execute(
            select(Datasource.type).where(Datasource.is_active == True)
        )
        types = [row[0] for row in type_result.all()]
        type_stats = {}
        for db_type in types:
            type_stats[db_type] = type_stats.get(db_type, 0) + 1
        
        # 连接状态统计
        status_result = await self.db.execute(
            select(Datasource.connection_status).where(Datasource.is_active == True)
        )
        statuses = [row[0] for row in status_result.all()]
        status_stats = {}
        for status in statuses:
            status_stats[status] = status_stats.get(status, 0) + 1
        
        return {
            "total": total,
            "active": active,
            "inactive": total - active,
            "by_type": type_stats,
            "by_status": status_stats
        }

    async def get_datasource_schema(self, datasource_id: int) -> Dict[str, Any]:
        """获取数据源结构信息"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 解密密码
            password = None
            if datasource.password:
                password = decrypt_password(datasource.password)
            
            # 创建数据库适配器
            config = {
                "host": datasource.host,
                "port": datasource.port,
                "database": datasource.database,
                "username": datasource.username,
                "password": password,
                "connection_params": json.loads(datasource.connection_params) if datasource.connection_params else {}
            }
            
            adapter = DatabaseAdapterFactory.create_adapter(datasource.type, config)
            schema_info = await adapter.get_schema_info()
            await adapter.close()
            
            return schema_info
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"获取数据源结构失败: {str(e)}"
            )

    async def execute_query(self, datasource_id: int, query: str) -> Dict[str, Any]:
        """执行数据源查询"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 解密密码
            password = None
            if datasource.password:
                password = decrypt_password(datasource.password)
            
            # 创建数据库适配器
            config = {
                "host": datasource.host,
                "port": datasource.port,
                "database": datasource.database,
                "username": datasource.username,
                "password": password,
                "connection_params": json.loads(datasource.connection_params) if datasource.connection_params else {}
            }
            
            adapter = DatabaseAdapterFactory.create_adapter(datasource.type, config)
            result = await adapter.execute_query(query)
            await adapter.close()
            
            return result
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"查询执行失败: {str(e)}"
            )

    async def get_datasource_tables(self, datasource_id: int) -> List[str]:
        """获取数据源表/集合列表"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 解密密码
            password = None
            if datasource.password:
                password = decrypt_password(datasource.password)
            
            # 创建数据库适配器
            config = {
                "host": datasource.host,
                "port": datasource.port,
                "database": datasource.database,
                "username": datasource.username,
                "password": password,
                "connection_params": json.loads(datasource.connection_params) if datasource.connection_params else {}
            }
            
            adapter = DatabaseAdapterFactory.create_adapter(datasource.type, config)
            tables = await adapter.get_tables()
            await adapter.close()
            
            return tables
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"获取表列表失败: {str(e)}"
            )

    async def get_supported_datasource_types(self) -> List[str]:
        """获取支持的数据源类型"""
        return DatabaseAdapterFactory.get_supported_types()

    # ...existing code...
    async def sync_datasource(self, datasource_id: int) -> Dict[str, Any]:
        """同步数据源数据"""
        datasource = await self.get_datasource_by_id(datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据源不存在"
            )
        
        try:
            # 这里可以实现具体的数据同步逻辑
            # 比如同步表结构、统计信息等
            
            # 更新同步时间
            datasource.last_sync_at = datetime.utcnow()
            await self.db.commit()
            
            return {
                "success": True,
                "message": "同步成功",
                "sync_time": datasource.last_sync_at
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"同步失败: {str(e)}"
            }

    async def get_datasource_types(self) -> List[Dict[str, str]]:
        """获取支持的数据源类型"""
        return [
            {"value": "postgresql", "label": "PostgreSQL"},
            {"value": "mysql", "label": "MySQL"},
            {"value": "redis", "label": "Redis"},
            {"value": "mongodb", "label": "MongoDB"},
            {"value": "sqlite", "label": "SQLite"},
            {"value": "oracle", "label": "Oracle"},
            {"value": "sqlserver", "label": "SQL Server"},
        ]

    async def get_datasource_statistics(self) -> Dict[str, Any]:
        """获取数据源统计信息"""
        # 总数统计
        total_result = await self.db.execute(select(Datasource.id))
        total = len(total_result.all())
        
        # 活跃数据源统计
        active_result = await self.db.execute(
            select(Datasource.id).where(Datasource.is_active == True)
        )
        active = len(active_result.all())
        
        # 按类型统计
        type_result = await self.db.execute(
            select(Datasource.type).where(Datasource.is_active == True)
        )
        types = [row[0] for row in type_result.all()]
        type_stats = {}
        for db_type in types:
            type_stats[db_type] = type_stats.get(db_type, 0) + 1
        
        # 连接状态统计
        status_result = await self.db.execute(
            select(Datasource.connection_status).where(Datasource.is_active == True)
        )
        statuses = [row[0] for row in status_result.all()]
        status_stats = {}
        for status in statuses:
            status_stats[status] = status_stats.get(status, 0) + 1
        
        return {
            "total": total,
            "active": active,
            "inactive": total - active,
            "by_type": type_stats,
            "by_status": status_stats
        }
