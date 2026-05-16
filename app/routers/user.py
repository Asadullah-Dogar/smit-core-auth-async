from fastapi import APIRouter, Depends
from app.models.user import User
from app.schemas.user import UserRegistrationResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRegistrationResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Fetches the protected user profile metrics cleanly. 
    This route is completely locked down by the zero-trust dependency.
    """
    # Because the dependency already did all the hard work (token extraction, 
    # blacklist checking, DB querying), we simply return the injected user object!
    return current_user