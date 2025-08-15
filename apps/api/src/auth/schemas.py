# 认证相关数据模式
# 定义API请求和响应的Pydantic模式

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """登录请求模式"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """登录响应模式"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserInfo(BaseModel):
    """用户信息模式"""
    id: str
    email: str
    full_name: str | None = None