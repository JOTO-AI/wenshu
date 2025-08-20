from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.models import Permission
from app.schemas import PermissionCreate, PermissionUpdate


class PermissionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_permission_by_id(self, permission_id: int) -> Optional[Permission]:
        """根据ID获取权限"""
        result = await self.db.execute(
            select(Permission)
            .options(selectinload(Permission.children))
            .where(Permission.id == permission_id)
        )
        return result.scalar_one_or_none()

    async def get_permission_by_name(self, name: str) -> Optional[Permission]:
        """根据名称获取权限"""
        result = await self.db.execute(
            select(Permission).where(Permission.name == name)
        )
        return result.scalar_one_or_none()

    async def get_permissions(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        resource: Optional[str] = None,
        action: Optional[str] = None,
        is_active: Optional[bool] = None,
        parent_id: Optional[int] = None
    ) -> tuple[List[Permission], int]:
        """获取权限列表"""
        query = select(Permission).options(selectinload(Permission.children))
        
        # 构建过滤条件
        filters = []
        if search:
            filters.append(
                or_(
                    Permission.name.ilike(f"%{search}%"),
                    Permission.description.ilike(f"%{search}%"),
                    Permission.resource.ilike(f"%{search}%"),
                    Permission.action.ilike(f"%{search}%")
                )
            )
        if resource:
            filters.append(Permission.resource == resource)
        if action:
            filters.append(Permission.action == action)
        if is_active is not None:
            filters.append(Permission.is_active == is_active)
        if parent_id is not None:
            filters.append(Permission.parent_id == parent_id)
        
        if filters:
            query = query.where(and_(*filters))
        
        # 获取总数
        count_result = await self.db.execute(
            select(Permission.id).where(and_(*filters)) if filters else select(Permission.id)
        )
        total = len(count_result.all())
        
        # 获取分页数据
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        permissions = result.scalars().all()
        
        return list(permissions), total

    async def create_permission(self, permission_data: PermissionCreate) -> Permission:
        """创建权限"""
        # 检查权限名是否已存在
        existing_permission = await self.get_permission_by_name(permission_data.name)
        if existing_permission:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="权限名已存在"
            )
        
        # 如果有父权限，检查父权限是否存在
        if permission_data.parent_id:
            parent_permission = await self.get_permission_by_id(permission_data.parent_id)
            if not parent_permission:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="父权限不存在"
                )
        
        # 创建权限
        permission = Permission(**permission_data.model_dump())
        
        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)
        
        return permission

    async def update_permission(self, permission_id: int, permission_data: PermissionUpdate) -> Permission:
        """更新权限"""
        permission = await self.get_permission_by_id(permission_id)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="权限不存在"
            )
        
        # 检查权限名是否被其他权限使用
        if permission_data.name and permission_data.name != permission.name:
            existing_permission = await self.get_permission_by_name(permission_data.name)
            if existing_permission:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="权限名已被其他权限使用"
                )
        
        # 检查父权限
        if permission_data.parent_id and permission_data.parent_id != permission.parent_id:
            if permission_data.parent_id == permission.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="不能将自己设为父权限"
                )
            
            parent_permission = await self.get_permission_by_id(permission_data.parent_id)
            if not parent_permission:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="父权限不存在"
                )
        
        # 更新权限信息
        for field, value in permission_data.model_dump(exclude_unset=True).items():
            setattr(permission, field, value)
        
        await self.db.commit()
        await self.db.refresh(permission)
        
        return permission

    async def delete_permission(self, permission_id: int) -> bool:
        """删除权限"""
        permission = await self.get_permission_by_id(permission_id)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="权限不存在"
            )
        
        # 检查是否有子权限
        if permission.children:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="存在子权限，无法删除"
            )
        
        # 检查是否有角色关联此权限
        if permission.roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="存在关联角色，无法删除权限"
            )
        
        await self.db.delete(permission)
        await self.db.commit()
        
        return True

    async def get_permission_tree(self) -> List[Dict[str, Any]]:
        """获取权限树"""
        # 获取所有权限
        result = await self.db.execute(
            select(Permission)
            .options(selectinload(Permission.children))
            .where(Permission.is_active == True)
        )
        permissions = result.scalars().all()
        
        # 构建权限字典
        permission_dict = {p.id: p for p in permissions}
        
        # 构建树结构
        def build_tree(parent_id: Optional[int] = None) -> List[Dict[str, Any]]:
            tree = []
            for permission in permissions:
                if permission.parent_id == parent_id:
                    node = {
                        "id": permission.id,
                        "name": permission.name,
                        "resource": permission.resource,
                        "action": permission.action,
                        "description": permission.description,
                        "children": build_tree(permission.id)
                    }
                    tree.append(node)
            return tree
        
        return build_tree()

    async def get_permissions_by_resource(self, resource: str) -> List[Permission]:
        """根据资源获取权限"""
        result = await self.db.execute(
            select(Permission)
            .where(and_(Permission.resource == resource, Permission.is_active == True))
        )
        return result.scalars().all()

    async def get_permissions_by_action(self, action: str) -> List[Permission]:
        """根据操作获取权限"""
        result = await self.db.execute(
            select(Permission)
            .where(and_(Permission.action == action, Permission.is_active == True))
        )
        return result.scalars().all()

    async def get_root_permissions(self) -> List[Permission]:
        """获取根权限（没有父权限的权限）"""
        result = await self.db.execute(
            select(Permission)
            .options(selectinload(Permission.children))
            .where(and_(Permission.parent_id.is_(None), Permission.is_active == True))
        )
        return result.scalars().all()

    async def init_default_permissions(self):
        """初始化默认权限"""
        default_permissions = [
            # 数据源权限
            {"name": "数据源管理", "resource": "datasources", "action": "manage", "description": "数据源管理权限"},
            {"name": "查看数据源", "resource": "datasources", "action": "read", "description": "查看数据源列表"},
            {"name": "创建数据源", "resource": "datasources", "action": "create", "description": "创建新数据源"},
            {"name": "更新数据源", "resource": "datasources", "action": "update", "description": "更新数据源信息"},
            {"name": "删除数据源", "resource": "datasources", "action": "delete", "description": "删除数据源"},
            {"name": "测试数据源连接", "resource": "datasources", "action": "test", "description": "测试数据源连接"},
            {"name": "同步数据源", "resource": "datasources", "action": "sync", "description": "同步数据源数据"},
            
            # 用户权限
            {"name": "用户管理", "resource": "users", "action": "manage", "description": "用户管理权限"},
            {"name": "查看用户", "resource": "users", "action": "read", "description": "查看用户列表"},
            {"name": "创建用户", "resource": "users", "action": "create", "description": "创建新用户"},
            {"name": "更新用户", "resource": "users", "action": "update", "description": "更新用户信息"},
            {"name": "删除用户", "resource": "users", "action": "delete", "description": "删除用户"},
            {"name": "重置密码", "resource": "users", "action": "reset_password", "description": "重置用户密码"},
            
            # 角色权限
            {"name": "角色管理", "resource": "roles", "action": "manage", "description": "角色管理权限"},
            {"name": "查看角色", "resource": "roles", "action": "read", "description": "查看角色列表"},
            {"name": "创建角色", "resource": "roles", "action": "create", "description": "创建新角色"},
            {"name": "更新角色", "resource": "roles", "action": "update", "description": "更新角色信息"},
            {"name": "删除角色", "resource": "roles", "action": "delete", "description": "删除角色"},
            {"name": "分配权限", "resource": "roles", "action": "assign_permissions", "description": "为角色分配权限"},
            
            # 权限管理
            {"name": "权限管理", "resource": "permissions", "action": "manage", "description": "权限管理权限"},
            {"name": "查看权限", "resource": "permissions", "action": "read", "description": "查看权限列表"},
            {"name": "创建权限", "resource": "permissions", "action": "create", "description": "创建新权限"},
            {"name": "更新权限", "resource": "permissions", "action": "update", "description": "更新权限信息"},
            {"name": "删除权限", "resource": "permissions", "action": "delete", "description": "删除权限"},
        ]
        
        for perm_data in default_permissions:
            existing = await self.get_permission_by_name(perm_data["name"])
            if not existing:
                permission = Permission(**perm_data)
                self.db.add(permission)
        
        await self.db.commit()
