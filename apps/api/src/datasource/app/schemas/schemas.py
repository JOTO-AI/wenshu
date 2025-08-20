from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# 用户相关模式
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=100)
    position: Optional[str] = Field(None, max_length=100)
    avatar: Optional[str] = Field(None, max_length=500)
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=100)
    position: Optional[str] = Field(None, max_length=100)
    avatar: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    roles: List["RoleRead"] = []

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResetPassword(BaseModel):
    new_password: str = Field(..., min_length=6, max_length=100)


# 角色相关模式
class RoleBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    is_active: bool = True


class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    is_active: Optional[bool] = None


class RoleRead(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    permissions: List["PermissionRead"] = []

    class Config:
        from_attributes = True


class RolePermissionUpdate(BaseModel):
    permission_ids: List[int]


# 权限相关模式
class PermissionBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    resource: str = Field(..., min_length=2, max_length=50)
    action: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    parent_id: Optional[int] = None
    is_active: bool = True


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    resource: Optional[str] = Field(None, min_length=2, max_length=50)
    action: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None


class PermissionRead(PermissionBase):
    id: int
    created_at: datetime
    children: Optional[List["PermissionRead"]] = None

    @validator('children', pre=True, always=True)
    def validate_children(cls, v):
        return v if v is not None else []

    class Config:
        from_attributes = True


class PermissionTree(PermissionRead):
    children: Optional[List["PermissionTree"]] = None

    @validator('children', pre=True, always=True)
    def validate_children(cls, v):
        return v if v is not None else []


# 数据源相关模式
class DatasourceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    type: str = Field(..., min_length=2, max_length=50)
    host: str = Field(..., min_length=1, max_length=255)
    port: int = Field(..., ge=1, le=65535)
    database: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, max_length=100)
    connection_params: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


class DatasourceCreate(DatasourceBase):
    password: Optional[str] = Field(None, max_length=255)


class DatasourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    type: Optional[str] = Field(None, min_length=2, max_length=50)
    host: Optional[str] = Field(None, min_length=1, max_length=255)
    port: Optional[int] = Field(None, ge=1, le=65535)
    database: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, max_length=255)
    connection_params: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class DatasourceRead(DatasourceBase):
    id: int
    creator_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_sync_at: Optional[datetime] = None
    connection_status: str
    last_test_at: Optional[datetime] = None
    creator: Optional[UserRead] = None

    class Config:
        from_attributes = True


class DatasourceTestConnection(BaseModel):
    success: bool
    message: str
    response_time: Optional[float] = None


# 认证相关模式
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserRead


# 通用响应模式
class Response(BaseModel):
    success: bool = True
    message: str = "操作成功"
    data: Optional[dict] = None


class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int


# 更新前向引用
UserRead.model_rebuild()
RoleRead.model_rebuild()
PermissionRead.model_rebuild()
PermissionTree.model_rebuild()
