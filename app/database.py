from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy 2.0 models."""
    pass


# Create the async engine without blocking sync drivers
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    # Connection pool settings for performance
    pool_size=20,
    max_overflow=10
)

# Create a session factory
AsyncSessionFactory = async_sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

async def get_db_session():
    """Dependency to provide a database session for routes."""
    async with AsyncSessionFactory() as session:
        yield session