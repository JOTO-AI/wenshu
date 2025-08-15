# 认证相关依赖注入
# 定义认证相关的FastAPI依赖，如获取当前用户等

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()


async def get_current_user(token: str = Depends(security)):
    """获取当前用户"""
    # TODO: 实现从token获取当前用户的逻辑
    # 验证token并返回用户信息
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="认证功能待实现"
    )