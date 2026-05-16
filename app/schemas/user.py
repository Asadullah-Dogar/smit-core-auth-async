from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# 1. Account Creation Schema
class UserRegistrationResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime  # Pydantic v2 automatically converts this to ISO 8601 string

    # This config tells Pydantic to read data directly from the SQLAlchemy User model
    model_config = ConfigDict(from_attributes=True)

# 2. Secure Authentication Token Schema
class TokenExchangeResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # Spec explicitly requires this to default to "bearer"

# 3. Standard Operational Message Schema
class StandardActionResponse(BaseModel):
    detail: str

# Input schema for Registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Input schema for Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str