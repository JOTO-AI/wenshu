# 用户相关数据模型
# 定义用户、角色、权限等数据库模型

from enum import Enum

# TODO: 添加用户相关的数据库模型
# 例如：User, Role, Permission等


class UserRole(str, Enum):
    """用户角色枚举"""
    CLIENT = "CLIENT"
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"


class User:
    """用户模型 (placeholder)"""
    pass


class Role:
    """角色模型 (placeholder)"""
    pass


class Permission:
    """权限模型 (placeholder)"""
    pass