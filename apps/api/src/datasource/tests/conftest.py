"""
测试配置模块
"""
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.database import get_db, Base
from main import app

# 测试数据库配置
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# 创建测试引擎
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    class_=AsyncSession
)


async def override_get_db():
    """覆盖依赖以使用测试数据库"""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def setup_test_db():
    """设置测试数据库"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client():
    """异步客户端"""
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def client():
    """同步客户端"""
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
async def db_session():
    """测试数据库会话"""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def test_user_data():
    """测试用户数据"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User",
        "is_active": True,
        "is_verified": True
    }


@pytest.fixture
async def test_datasource_data():
    """测试数据源数据"""
    return {
        "name": "test_datasource",
        "type": "postgresql",
        "host": "localhost",
        "port": 5432,
        "database": "test_db",
        "username": "test_user",
        "password": "test_pass",
        "description": "Test datasource"
    }
