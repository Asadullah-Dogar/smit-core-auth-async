import uuid
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from app.config import settings

# Cryptographic standards
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(subject: str | int) -> str:
    """Create a short-lived access token signed with ACCESS_SECRET_KEY."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: Dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid.uuid4()),
        "type": "access",
    }
    return jwt.encode(payload, settings.ACCESS_SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: str | int) -> str:
    """Create a long-lived refresh token signed with REFRESH_SECRET_KEY."""
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload: Dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid.uuid4()),
        "type": "refresh",
    }
    return jwt.encode(payload, settings.REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, expected_type: str) -> Dict[str, Any]:
    """Decode and validate token type and expiration."""
    secret = settings.ACCESS_SECRET_KEY if expected_type == "access" else settings.REFRESH_SECRET_KEY
    payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError(f"Expected {expected_type} token")
    return payload