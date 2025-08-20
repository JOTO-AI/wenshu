"""
用户相关接口测试
"""
import pytest
from httpx import AsyncClient
from fastapi import status


class TestUserAPI:
    """用户API测试类"""
    
    @pytest.mark.asyncio
    async def test_create_user(self, async_client: AsyncClient, test_user_data):
        """测试创建用户"""
        response = await async_client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["username"] == test_user_data["username"]
        assert "id" in data
        assert "hashed_password" not in data
    
    @pytest.mark.asyncio
    async def test_login_user(self, async_client: AsyncClient, test_user_data):
        """测试用户登录"""
        # 先创建用户
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        
        # 登录
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = await async_client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_get_current_user(self, async_client: AsyncClient, test_user_data):
        """测试获取当前用户信息"""
        # 创建用户并登录
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        login_response = await async_client.post("/api/v1/auth/login", data=login_data)
        token = login_response.json()["access_token"]
        
        # 获取当前用户信息
        headers = {"Authorization": f"Bearer {token}"}
        response = await async_client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == test_user_data["email"]
    
    @pytest.mark.asyncio
    async def test_list_users(self, async_client: AsyncClient, test_user_data):
        """测试获取用户列表"""
        # 创建用户并登录
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        login_response = await async_client.post("/api/v1/auth/login", data=login_data)
        token = login_response.json()["access_token"]
        
        # 获取用户列表
        headers = {"Authorization": f"Bearer {token}"}
        response = await async_client.get("/api/v1/users/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert len(data["items"]) > 0
