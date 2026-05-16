from fastapi import APIRouter, Depends, HTTPException, Header, status
from redis.asyncio import Redis

from app.redis import get_redis
from app.schemas.user import TokenExchangeResponse, StandardActionResponse
from app.services.jwt import create_access_token, create_refresh_token, decode_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/tokens", tags=["Token Management"])


@router.post("/refresh", response_model=TokenExchangeResponse)
async def refresh_session(refresh_token: str = Header(...)):
    """Rotates tokens without requiring re-authentication."""
    try:
        # Strict validation: Only accept tokens explicitly signed as "refresh"
        payload = decode_token(refresh_token, expected_type="refresh")
        user_id = payload.get("sub")

        return {
            "access_token": create_access_token(user_id),
            "refresh_token": create_refresh_token(user_id),
            "token_type": "bearer"  # nosec B105
        }
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token.")


@router.post("/logout", response_model=StandardActionResponse)
async def logout(access_token: str = Header(...), redis_client: Redis = Depends(get_redis)):
    """Revokes the current access token by saving its fingerprint to the fast memory blacklist."""
    try:
        payload = decode_token(access_token, expected_type="access")
        jti = payload.get("jti")

        # Calculate remaining lifespan in seconds to avoid storing dead tokens forever
        ttl = ACCESS_TOKEN_EXPIRE_MINUTES * 60

        # Save the token fingerprint to Redis
        await redis_client.setex(f"blacklist:{jti}", ttl, "true")

        return {"detail": "Revocation complete"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")