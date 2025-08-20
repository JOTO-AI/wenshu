import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal
from app.models import User
from sqlalchemy import select


async def test_db_connection():
    """测试数据库连接"""
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(User))
            users = result.scalars().all()
            print(f"数据库连接成功！当前用户数量: {len(users)}")
            for user in users:
                print(f"  用户: {user.username} ({user.email})")
            return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(test_db_connection())
