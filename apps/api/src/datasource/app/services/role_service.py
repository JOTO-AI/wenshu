from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.models import Role, Permission, User
from app.schemas import RoleCreate, RoleUpdate
from app.core.casbin import casbin_service


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """根据ID获取角色"""
        result = await self.db.execute(
            select(Role)
            .options(selectinload(Role.permissions), selectinload(Role.users))
            .where(Role.id == role_id)
        )
        return result.scalar_one_or_none()

    async def get_role_by_name(self, name: str) -> Optional[Role]:
        """根据名称获取角色"""
        result = await self.db.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.name == name)
        )
        return result.scalar_one_or_none()

    async def get_roles(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> tuple[List[Role], int]:
        """获取角色列表"""
        query = select(Role).options(selectinload(Role.permissions))
        
        # 构建过滤条件
        filters = []
        if search:
            filters.append(
                or_(
                    Role.name.ilike(f"%{search}%"),
                    Role.description.ilike(f"%{search}%")
                )
            )
        if is_active is not None:
            filters.append(Role.is_active == is_active)
        
        if filters:
            query = query.where(and_(*filters))
        
        # 获取总数
        count_result = await self.db.execute(
            select(Role.id).where(and_(*filters)) if filters else select(Role.id)
        )
        total = len(count_result.all())
        
        # 获取分页数据
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        roles = result.scalars().all()
        
        return list(roles), total

    async def create_role(self, role_data: RoleCreate) -> Role:
        """创建角色"""
        # 检查角色名是否已存在
        existing_role = await self.get_role_by_name(role_data.name)
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="角色名已存在"
            )
        
        # 创建角色
        role = Role(
            name=role_data.name,
            description=role_data.description,
            is_active=role_data.is_active
        )
        
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        
        # 分配权限
        if role_data.permission_ids:
            await self.assign_permissions(role.id, role_data.permission_ids)
        
        return role

    async def update_role(self, role_id: int, role_data: RoleUpdate) -> Role:
        """更新角色"""
        role = await self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="角色不存在"
            )
        
        # 检查角色名是否被其他角色使用
        if role_data.name and role_data.name != role.name:
            existing_role = await self.get_role_by_name(role_data.name)
            if existing_role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="角色名已被其他角色使用"
                )
        
        # 更新角色信息
        for field, value in role_data.model_dump(exclude_unset=True).items():
            setattr(role, field, value)
        
        await self.db.commit()
        await self.db.refresh(role)
        
        return role

    async def delete_role(self, role_id: int) -> bool:
        """删除角色"""
        role = await self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="角色不存在"
            )
        
        # 检查是否有用户关联此角色
        if role.users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="存在关联用户，无法删除角色"
            )
        
        await self.db.delete(role)
        await self.db.commit()
        
        return True

    async def assign_permissions(self, role_id: int, permission_ids: List[int]) -> Role:
        """为角色分配权限"""
        role = await self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="角色不存在"
            )
        
        # 获取权限
        result = await self.db.execute(
            select(Permission).where(Permission.id.in_(permission_ids))
        )
        permissions = result.scalars().all()
        
        # 清除现有权限并添加新权限
        role.permissions.clear()
        
        # 从Casbin中移除旧权限
        for perm in role.permissions:
            casbin_service.remove_permission(role.name, perm.resource, perm.action)
        
        # 添加新权限
        for permission in permissions:
            role.permissions.append(permission)
            # 同步到Casbin
            casbin_service.add_permission(role.name, permission.resource, permission.action)
        
        await self.db.commit()
        await self.db.refresh(role)
        
        # 保存Casbin策略
        casbin_service.save_policy()
        
        return role

    async def get_role_permissions(self, role_id: int) -> List[Permission]:
        """获取角色权限"""
        role = await self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="角色不存在"
            )
        
        return role.permissions

    async def get_role_users(self, role_id: int) -> List[User]:
        """获取角色下的用户"""
        role = await self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="角色不存在"
            )
        
        return role.users
