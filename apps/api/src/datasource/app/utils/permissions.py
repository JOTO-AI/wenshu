from functools import wraps
from fastapi import HTTPException, status
from typing import Any

from app.core.casbin import casbin_service


def require_permission(resource: str, action: str):
    """权限装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 从kwargs中获取current_user
            current_user = kwargs.get('current_user')
            if not current_user:
                # 如果没有current_user，尝试从args中获取
                for arg in args:
                    if hasattr(arg, 'id') and hasattr(arg, 'is_superuser'):  # User object
                        current_user = arg
                        break
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="未认证的用户"
                )
            
            # 超级用户拥有所有权限
            if current_user.is_superuser:
                return await func(*args, **kwargs)
            
            # 检查权限
            has_permission = await casbin_service.enforce(
                str(current_user.id), resource, action
            )
            
            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="权限不足"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_role(role_name: str):
    """角色装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 从kwargs中获取current_user
            current_user = kwargs.get('current_user')
            if not current_user:
                # 如果没有current_user，尝试从args中获取
                for arg in args:
                    if hasattr(arg, 'id') and hasattr(arg, 'is_superuser'):  # User object
                        current_user = arg
                        break
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="未认证的用户"
                )
            
            # 超级用户拥有所有角色
            if current_user.is_superuser:
                return await func(*args, **kwargs)
            
            # 检查角色
            user_roles = [role.name for role in current_user.roles]
            if role_name not in user_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="角色权限不足"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


class PermissionChecker:
    """权限检查器类"""
    
    def __init__(self, resource: str, action: str):
        self.resource = resource
        self.action = action
    
    async def __call__(self, current_user: Any) -> Any:
        """检查权限"""
        # 超级用户拥有所有权限
        if current_user.is_superuser:
            return current_user
        
        # 检查权限
        has_permission = await casbin_service.enforce(
            str(current_user.id), self.resource, self.action
        )
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        return current_user

class RoleChecker:
    """角色检查器类"""

    def __init__(self, role_name: str):
        self.role_name = role_name

    async def __call__(self, current_user: Any) -> Any:
        """检查角色"""
        # 超级用户拥有所有角色
        if current_user.is_superuser:
            return current_user
        
        # 检查角色
        user_roles = [role.name for role in current_user.roles]
        if self.role_name not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="角色权限不足"
            )
        
        return current_user


# 常用权限检查器实例
check_datasource_read = PermissionChecker("datasources", "read")
check_datasource_write = PermissionChecker("datasources", "write")
check_datasource_delete = PermissionChecker("datasources", "delete")

check_user_read = PermissionChecker("users", "read")
check_user_write = PermissionChecker("users", "write")
check_user_delete = PermissionChecker("users", "delete")

check_role_read = PermissionChecker("roles", "read")
check_role_write = PermissionChecker("roles", "write")
check_role_delete = PermissionChecker("roles", "delete")

check_permission_read = PermissionChecker("permissions", "read")
check_permission_write = PermissionChecker("permissions", "write")

# 常用角色检查器实例
check_admin_role = RoleChecker("admin")
check_user_role = RoleChecker("user")
