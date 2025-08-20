import casbin
from casbin_sqlalchemy_adapter import Adapter
from app.core.config import settings
from app.core.database import sync_engine
from typing import Optional


class CasbinService:
    def __init__(self):
        self.adapter = None
        self.enforcer = None
        self._initialize()
    
    def _initialize(self):
        """初始化Casbin"""
        try:
            # 使用SQLAlchemy适配器
            self.adapter = Adapter(sync_engine)
            
            # 创建执行器
            self.enforcer = casbin.Enforcer(settings.casbin_model_path, self.adapter)
            
            # 加载策略
            self.enforcer.load_policy()
            
        except Exception as e:
            print(f"Casbin初始化失败: {e}")
            # 如果数据库适配器失败，使用文件适配器
            self.enforcer = casbin.Enforcer(
                settings.casbin_model_path, 
                settings.casbin_policy_path
            )
    def check_permission(self, user: str, resource: str, action: str) -> bool:
        """检查权限"""
        if not self.enforcer:
            return False
        return self.enforcer.enforce(user, resource, action)
    
    async def enforce(self, user: str, resource: str, action: str) -> bool:
        """异步检查权限（与check_permission相同）"""
        return self.check_permission(user, resource, action)
    
    def add_permission(self, role: str, resource: str, action: str) -> bool:
        """添加权限"""
        if not self.enforcer:
            return False
        return self.enforcer.add_policy(role, resource, action)
    
    def remove_permission(self, role: str, resource: str, action: str) -> bool:
        """移除权限"""
        if not self.enforcer:
            return False
        return self.enforcer.remove_policy(role, resource, action)
    
    def add_role_for_user(self, user: str, role: str) -> bool:
        """为用户添加角色"""
        if not self.enforcer:
            return False
        return self.enforcer.add_role_for_user(user, role)
    
    def remove_role_for_user(self, user: str, role: str) -> bool:
        """移除用户角色"""
        if not self.enforcer:
            return False
        return self.enforcer.delete_role_for_user(user, role)
    
    def get_roles_for_user(self, user: str) -> list:
        """获取用户角色"""
        if not self.enforcer:
            return []
        return self.enforcer.get_roles_for_user(user)
    
    def get_users_for_role(self, role: str) -> list:
        """获取角色下的用户"""
        if not self.enforcer:
            return []
        return self.enforcer.get_users_for_role(role)
    
    def save_policy(self):
        """保存策略"""
        if self.enforcer:
            self.enforcer.save_policy()


# 全局Casbin服务实例
casbin_service = CasbinService()
