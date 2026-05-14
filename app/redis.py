import redis.asyncio as redis
from app.config import settings

# Initialize the Redis client (to be connected in lifespan)
redis_client = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)

async def get_redis():
    """Dependency to provide the Redis client."""
    return redis_client