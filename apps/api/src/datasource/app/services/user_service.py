from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.models import User, Role
from app.schemas import UserCreate, UserUpdate, UserResetPassword
from app.core.security import get_password_hash, verify_password
from app.core.casbin import casbin_service
import uuid


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """根据ID获取用户"""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> tuple[List[User], int]:
        """获取用户列表"""
        query = select(User).options(selectinload(User.roles))
        
        # 构建过滤条件
        filters = []
        if search:
            filters.append(
                or_(
                    User.username.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                    User.full_name.ilike(f"%{search}%")
                )
            )
        if is_active is not None:
            filters.append(User.is_active == is_active)
        
        if filters:
            query = query.where(and_(*filters))
        
        # 获取总数
        count_result = await self.db.execute(
            select(User.id).where(and_(*filters)) if filters else select(User.id)
        )
        total = len(count_result.all())
        
        # 获取分页数据
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return list(users), total

    async def create_user(self, user_data: UserCreate) -> User:
        """创建用户"""
        # 检查邮箱是否已存在
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被使用"
            )
        
        # 检查用户名是否已存在
        existing_username = await self.get_user_by_username(user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已被使用"
            )
        
        # 创建用户
        hashed_password = get_password_hash(user_data.password)
        user = User(
            **user_data.model_dump(exclude={"password"}),
            hashed_password=hashed_password
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user

    async def update_user(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        """更新用户"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 检查邮箱是否被其他用户使用
        if user_data.email and user_data.email != user.email:
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被其他用户使用"
                )
        
        # 检查用户名是否被其他用户使用
        if user_data.username and user_data.username != user.username:
            existing_username = await self.get_user_by_username(user_data.username)
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名已被其他用户使用"
                )
        
        # 更新用户信息
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user

    async def delete_user(self, user_id: uuid.UUID) -> bool:
        """删除用户"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 软删除：设置为非活跃状态
        user.is_active = False
        await self.db.commit()
        
        return True

    async def reset_password(self, user_id: uuid.UUID, password_data: UserResetPassword) -> bool:
        """重置密码"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        user.hashed_password = get_password_hash(password_data.new_password)
        await self.db.commit()
        
        return True

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """用户认证"""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

    async def assign_roles(self, user_id: uuid.UUID, role_ids: List[int]) -> User:
        """为用户分配角色"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 获取角色
        result = await self.db.execute(
            select(Role).where(Role.id.in_(role_ids))
        )
        roles = result.scalars().all()
        
        # 清除现有角色并添加新角色
        user.roles.clear()
        for role in roles:
            user.roles.append(role)
            # 同步到Casbin
            casbin_service.add_role_for_user(str(user.id), role.name)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user

    async def check_permission(self, user_id: uuid.UUID, resource: str, action: str) -> bool:
        """检查用户权限"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        # 超级用户拥有所有权限
        if user.is_superuser:
            return True
        
        # 检查Casbin权限
        return casbin_service.check_permission(str(user.id), resource, action)
