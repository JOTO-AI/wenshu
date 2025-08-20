"""
数据源相关接口测试
"""
import pytest
from httpx import AsyncClient
from fastapi import status


class TestDatasourceAPI:
    """数据源API测试类"""
    
    async def _get_auth_headers(self, async_client: AsyncClient, test_user_data):
        """获取认证头"""
        # 创建用户并登录
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        login_response = await async_client.post("/api/v1/auth/login", data=login_data)
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    @pytest.mark.asyncio
    async def test_create_datasource(self, async_client: AsyncClient, test_user_data, test_datasource_data):
        """测试创建数据源"""
        headers = await self._get_auth_headers(async_client, test_user_data)
        
        response = await async_client.post("/api/v1/datasources/", json=test_datasource_data, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == test_datasource_data["name"]
        assert data["type"] == test_datasource_data["type"]
        assert "id" in data
        assert "password" not in data  # 密码不应该在返回中
    
    @pytest.mark.asyncio
    async def test_list_datasources(self, async_client: AsyncClient, test_user_data, test_datasource_data):
        """测试获取数据源列表"""
        headers = await self._get_auth_headers(async_client, test_user_data)
        
        # 创建数据源
        await async_client.post("/api/v1/datasources/", json=test_datasource_data, headers=headers)
        
        # 获取列表
        response = await async_client.get("/api/v1/datasources/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert len(data["items"]) > 0
    
    @pytest.mark.asyncio
    async def test_get_datasource(self, async_client: AsyncClient, test_user_data, test_datasource_data):
        """测试获取单个数据源"""
        headers = await self._get_auth_headers(async_client, test_user_data)
        
        # 创建数据源
        create_response = await async_client.post("/api/v1/datasources/", json=test_datasource_data, headers=headers)
        datasource_id = create_response.json()["id"]
        
        # 获取数据源
        response = await async_client.get(f"/api/v1/datasources/{datasource_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == datasource_id
        assert data["name"] == test_datasource_data["name"]
    
    @pytest.mark.asyncio
    async def test_update_datasource(self, async_client: AsyncClient, test_user_data, test_datasource_data):
        """测试更新数据源"""
        headers = await self._get_auth_headers(async_client, test_user_data)
        
        # 创建数据源
        create_response = await async_client.post("/api/v1/datasources/", json=test_datasource_data, headers=headers)
        datasource_id = create_response.json()["id"]
        
        # 更新数据源
        update_data = {"name": "updated_datasource", "description": "Updated description"}
        response = await async_client.put(f"/api/v1/datasources/{datasource_id}", json=update_data, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
    
    @pytest.mark.asyncio
    async def test_delete_datasource(self, async_client: AsyncClient, test_user_data, test_datasource_data):
        """测试删除数据源"""
        headers = await self._get_auth_headers(async_client, test_user_data)
        
        # 创建数据源
        create_response = await async_client.post("/api/v1/datasources/", json=test_datasource_data, headers=headers)
        datasource_id = create_response.json()["id"]
        
        # 删除数据源
        response = await async_client.delete(f"/api/v1/datasources/{datasource_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        
        # 验证已删除
        get_response = await async_client.get(f"/api/v1/datasources/{datasource_id}", headers=headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
