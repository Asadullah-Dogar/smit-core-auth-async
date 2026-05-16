import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.database import get_db_session, Base
from app.redis import get_redis
from app.config import settings

# 1. Use a separate SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine_test = create_async_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)
TestingSessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine_test, 
    class_=AsyncSession
)

# 2. Override the Database Dependency
async def override_get_db_session():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db_session] = override_get_db_session

# 3. Mock Redis for testing (so we don't need a real Redis server running for tests)
class MockRedis:
    def __init__(self):
        self.store = {}
    
    async def setex(self, key, time, value):
        self.store[key] = value
    
    async def get(self, key):
        return self.store.get(key)
    
    async def delete(self, key):
        self.store.pop(key, None)
    
    async def ping(self):
        return True

mock_redis = MockRedis()

async def override_get_redis():
    return mock_redis

app.dependency_overrides[get_redis] = override_get_redis

# 4. Setup and Teardown Fixtures
@pytest_asyncio.fixture(scope="function")
async def setup_test_db():
    """Creates fresh tables for each test and drops them after."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def async_client(setup_test_db):
    """Provides an async HTTP client to make requests to our FastAPI app."""
    # Clear Redis mock before each test
    mock_redis.store.clear()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client