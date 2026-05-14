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
from app.redis import redis_client

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
    await redis_client.ping()
    
    yield  # Application is running and serving requests
    
    # --- SHUTDOWN ---
    logger.info("Closing database engine connections...")
    await engine.dispose()
    
    logger.info("Closing Redis connection pool...")
    await redis_client.aclose()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    """Basic health check route to ensure the server is alive."""
    return {"status": "ok", "system": settings.PROJECT_NAME}