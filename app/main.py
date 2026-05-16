"""
Advanced Asynchronous Backend System (Enterprise Core)
------------------------------------------------------
Author: Asad Ullah Dogar
Reviewers: Sir Daniyal

Project Notes for Reviewers:
- This project utilizes a strict asynchronous execution model with non-blocking I/O.
- Pool lifecycle management (Database & Redis) is handled explicitly via the FastAPI lifespan context manager.
- Zero-Trust networking and stateless/stateful hybrid authentication are configured in subsequent phases.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import engine
from app import redis as app_redis
from app.routers.auth import router as auth_router
from app.routers.tokens import router as tokens_router
from app.routers.user import router as users_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events to manage connection pools.
    """
    # --- STARTUP ---
    logger.info("Initializing database connection pool...")
    # The DB engine is already created, but we can verify connectivity here if needed
    
    logger.info("Connecting to Redis fast memory layer...")
    # Try to use the configured Redis; on localhost failures fall back to fakeredis for local dev
    try:
        await app_redis.redis_client.ping()
    except Exception as e:
        # only fallback for local dev hosts
        url = settings.REDIS_URL or ""
        if "localhost" in url or "127.0.0.1" in url:
            logger.warning("Redis unavailable at %s, falling back to fakeredis: %s", url, e)
            try:
                import fakeredis.aioredis as fakeredis_aioredis

                fake = fakeredis_aioredis.FakeRedis()
                app_redis.redis_client = fake
                # verify fake client
                await app_redis.redis_client.ping()
            except Exception as fe:
                logger.exception("Failed to initialize fakeredis fallback: %s", fe)
                raise
        else:
            raise
    
    yield  # Application is running and serving requests
    
    # --- SHUTDOWN ---
    logger.info("Closing database engine connections...")
    await engine.dispose()
    
    logger.info("Closing Redis connection pool...")
    try:
        await app_redis.redis_client.aclose()
    except Exception:
        logger.exception("Error while closing Redis connection pool")

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Include the routers
app.include_router(auth_router)
app.include_router(tokens_router)
app.include_router(users_router)

@app.get("/health")
async def health_check():
    """Basic health check route to ensure the server is alive."""
    return {"status": "ok", "system": settings.PROJECT_NAME}