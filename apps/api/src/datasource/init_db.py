import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.services import UserService, RoleService, PermissionService
from app.schemas import UserCreate, RoleCreate, PermissionCreate
from app.models import User, Role, Permission
from app.core.casbin import casbin_service
from sqlalchemy import select
import uuid


async def init_database():
    """初始化数据库数据"""
    async with AsyncSessionLocal() as db:
        user_service = UserService(db)
        role_service = RoleService(db)
        permission_service = PermissionService(db)
        
        print("=== 初始化数据库数据 ===")
        
        # 检查是否已有数据
        existing_users = await db.execute(select(User))
        if existing_users.scalars().first():
            print("数据库已有用户数据，跳过初始化")
            return
        
        # 1. 创建权限
        print("创建权限...")
        permissions_data = [
            # 用户权限
            {"name": "用户读取", "resource": "users", "action": "read", "description": "读取用户信息"},
            {"name": "用户写入", "resource": "users", "action": "write", "description": "创建和更新用户"},
            {"name": "用户删除", "resource": "users", "action": "delete", "description": "删除用户"},
            
            # 角色权限
            {"name": "角色读取", "resource": "roles", "action": "read", "description": "读取角色信息"},
            {"name": "角色写入", "resource": "roles", "action": "write", "description": "创建和更新角色"},
            {"name": "角色删除", "resource": "roles", "action": "delete", "description": "删除角色"},
            
            # 权限管理权限
            {"name": "权限读取", "resource": "permissions", "action": "read", "description": "读取权限信息"},
            {"name": "权限写入", "resource": "permissions", "action": "write", "description": "创建和更新权限"},
            
            # 数据源权限
            {"name": "数据源读取", "resource": "datasources", "action": "read", "description": "读取数据源信息"},
            {"name": "数据源写入", "resource": "datasources", "action": "write", "description": "创建和更新数据源"},
            {"name": "数据源删除", "resource": "datasources", "action": "delete", "description": "删除数据源"},
        ]
        
        permissions = {}
        for perm_data in permissions_data:
            perm = await permission_service.create_permission(PermissionCreate(**perm_data))
            permissions[f"{perm_data['resource']}:{perm_data['action']}"] = perm
            print(f"  创建权限: {perm.name}")
        
        # 2. 创建角色
        print("\n创建角色...")
        
        # 管理员角色 - 拥有所有权限
        admin_role = await role_service.create_role(RoleCreate(
            name="admin",
            description="系统管理员，拥有所有权限"
        ))
        
        # 为管理员角色分配所有权限
        admin_permission_ids = [perm.id for perm in permissions.values()]
        await role_service.assign_permissions(admin_role.id, admin_permission_ids)
        print(f"  创建角色: {admin_role.name} (权限数: {len(admin_permission_ids)})")
        
        # 普通用户角色 - 只有读取权限
        user_role = await role_service.create_role(RoleCreate(
            name="user",
            description="普通用户，只有基本读取权限"
        ))
        
        # 为普通用户角色分配读取权限
        user_permission_ids = [
            permissions["users:read"].id,
            permissions["datasources:read"].id,
        ]
        await role_service.assign_permissions(user_role.id, user_permission_ids)
        print(f"  创建角色: {user_role.name} (权限数: {len(user_permission_ids)})")
        
        # 3. 创建管理员用户
        print("\n创建用户...")
        admin_user = await user_service.create_user(UserCreate(
            username="admin",
            email="admin@example.com",
            password="admin123",
            full_name="系统管理员",
            is_superuser=True
        ))
        
        # 为管理员用户分配管理员角色
        await user_service.assign_roles(admin_user.id, [admin_role.id])
        print(f"  创建用户: {admin_user.username} (超级用户)")
        
        # 创建测试用户
        test_user = await user_service.create_user(UserCreate(
            username="testuser",
            email="test@example.com",
            password="test123",
            full_name="测试用户"
        ))
        
        # 为测试用户分配普通用户角色
        await user_service.assign_roles(test_user.id, [user_role.id])
        print(f"  创建用户: {test_user.username} (普通用户)")
        
        # 4. 设置Casbin权限
        print("\n设置Casbin权限...")
        
        # 为管理员用户添加admin角色
        casbin_service.add_role_for_user(str(admin_user.id), "admin")
        print(f"  添加Casbin角色: {admin_user.username} -> admin")
        
        # 为测试用户添加user角色  
        casbin_service.add_role_for_user(str(test_user.id), "user")
        print(f"  添加Casbin角色: {test_user.username} -> user")
        
        # 保存Casbin策略
        casbin_service.save_policy()
        
        await db.commit()
        print("\n✓ 数据库初始化完成！")
        print(f"管理员账户: admin / admin123")
        print(f"测试账户: testuser / test123")


if __name__ == "__main__":
    asyncio.run(init_database())
