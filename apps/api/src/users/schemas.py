# 用户相关数据模式
# 定义用户管理API请求和响应的Pydantic模式

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import UserRole


class UserBase(BaseModel):
    """用户基础模式"""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    """用户创建模式"""
    password: str
    role: UserRole = UserRole.CLIENT


class UserUpdate(BaseModel):
    """用户更新模式"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase):
    """用户响应模式"""
    id: str
    role: UserRole
    created_at: datetime
    updated_at: datetime


class UserListResponse(BaseModel):
    """用户列表响应模式"""
    users: List[UserResponse]
    total: int
    skip: int
    limit: int