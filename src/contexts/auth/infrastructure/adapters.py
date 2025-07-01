from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.shared.infrastructure.database import get_db
from src.shared.domain.exceptions import UnauthorizedError
from src.contexts.auth.application.dtos import LoginDto, TokenDto
from src.contexts.auth.domain.services import AuthService
from src.contexts.users.infrastructure.repositories import SQLAlchemyUserRepository
from src.contexts.users.domain.services import PasswordService


router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Get authentication service instance."""
    user_repository = SQLAlchemyUserRepository(db)
    password_service = PasswordService()
    return AuthService(user_repository, password_service)


@router.post("/login", response_model=TokenDto)
async def login(
    login_data: LoginDto,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Authenticate user and return access token."""
    try:
        result = await auth_service.authenticate_user(login_data.email, login_data.password)
        return TokenDto(**result)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/verify")
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Verify JWT token."""
    try:
        payload = auth_service.verify_token(credentials.credentials)
        return {"valid": True, "user_id": payload.get("sub"), "email": payload.get("email")}
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) 