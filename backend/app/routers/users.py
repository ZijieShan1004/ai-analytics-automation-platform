from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()


# Return the current user profile.
@router.get("/me", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)) -> User:
    return current_user