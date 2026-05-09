from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    # Register a new user account.
    def register(self, payload: RegisterRequest) -> User:
        existing_user = self.user_repository.get_by_email(payload.email)

        if existing_user is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        hashed_password = get_password_hash(payload.password)
        return self.user_repository.create(payload.email, hashed_password, payload.full_name)

    # Authenticate a user and return a JWT token.
    def login(self, email: str, password: str) -> TokenResponse:
        user = self.user_repository.get_by_email(email)

        if user is None or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        token = create_access_token(str(user.id))
        return TokenResponse(access_token=token)