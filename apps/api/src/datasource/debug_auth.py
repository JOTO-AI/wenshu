import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal, get_redis
from app.services import UserService
from app.models import User, Role, Permission
from app.core.casbin import casbin_service
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def debug_user_permissions():
    """调试用户权限"""
    async with AsyncSessionLocal() as db:
        # 获取所有用户及其角色权限
        result = await db.execute(
            select(User)
            .options(
                selectinload(User.roles).selectinload(Role.permissions)
            )
        )
        users = result.scalars().all()
        
        print("=== 用户权限调试 ===")
        for user in users:
            print(f"\n用户: {user.username} (ID: {user.id})")
            print(f"  邮箱: {user.email}")
            print(f"  活跃状态: {user.is_active}")
            print(f"  超级用户: {user.is_superuser}")
            print(f"  角色数量: {len(user.roles)}")
            
            for role in user.roles:
                print(f"    角色: {role.name} (活跃: {role.is_active})")
                print(f"      权限数量: {len(role.permissions)}")
                
                for perm in role.permissions:
                    print(f"        权限: {perm.name} ({perm.resource}:{perm.action}) (活跃: {perm.is_active})")
        
        # 检查Redis中的token
        print("\n=== Redis Token 检查 ===")
        redis_client = await get_redis()
        for user in users:
            refresh_token = await redis_client.get(f"refresh_token:{user.id}")
            print(f"用户 {user.username} 的刷新token: {'存在' if refresh_token else '不存在'}")
        
        # 测试Casbin权限检查
        print("\n=== Casbin 权限检查 ===")
        for user in users:
            user_id = str(user.id)
            
            # 检查一些基本权限
            permissions_to_check = [
                ("users", "read"),
                ("users", "write"),
                ("datasources", "read"),
                ("roles", "read")
            ]
            
            print(f"\n用户 {user.username} ({user_id}) 的权限检查:")
            for resource, action in permissions_to_check:
                has_perm = await casbin_service.enforce(user_id, resource, action)
                print(f"  {resource}:{action} -> {'✓' if has_perm else '✗'}")
            
            # 检查用户的Casbin角色
            casbin_roles = casbin_service.get_roles_for_user(user_id)
            print(f"  Casbin角色: {casbin_roles}")


if __name__ == "__main__":
    asyncio.run(debug_user_permissions())
