from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.shared.infrastructure.database import get_db
from src.contexts.auth.domain.services import AuthService
from src.contexts.users.infrastructure.repositories import SQLAlchemyUserRepository
from src.contexts.users.domain.services import PasswordService
from src.shared.domain.exceptions import UnauthorizedError


security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Get authentication service instance."""
    user_repository = SQLAlchemyUserRepository(db)
    password_service = PasswordService()
    return AuthService(user_repository, password_service)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Get current authenticated user from JWT token."""
    try:
        payload = auth_service.verify_token(credentials.credentials)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user_id": user_id, "email": payload.get("email")}
    except UnauthorizedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_id(
    current_user: dict = Depends(get_current_user)
) -> str:
    """Get current user ID from authentication."""
    return current_user["user_id"] 