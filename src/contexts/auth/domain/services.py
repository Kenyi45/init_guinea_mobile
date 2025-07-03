from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from src.shared.domain.exceptions import UnauthorizedError
from src.contexts.users.domain.services import PasswordService
from src.contexts.users.domain.repositories import UserRepository
from src.shared.infrastructure.metrics import record_auth_attempt, record_jwt_token_issued
import os


class AuthService:
    """Domain service for authentication operations."""
    
    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    
    async def authenticate_user(self, email: str, password: str) -> dict:
        """Authenticate a user with email and password."""
        try:
            user = await self.user_repository.find_by_email(email)
            if not user:
                record_auth_attempt("invalid_credentials")
                raise UnauthorizedError("Invalid email or password")
            
            if not user.is_active:
                record_auth_attempt("inactive_account")
                raise UnauthorizedError("User account is inactive")
            
            if not self.password_service.verify_password(password, user.hashed_password.hashed_value):
                record_auth_attempt("invalid_password")
                raise UnauthorizedError("Invalid email or password")
            
            # Create access token
            access_token = self._create_access_token({"sub": user.id, "email": user.email.value})
            
            # Record successful authentication and token issuance
            record_auth_attempt("success")
            record_jwt_token_issued()
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user.id,
                "email": user.email.value,
                "expires_at": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            }
        except UnauthorizedError:
            # Re-raise UnauthorizedError without additional logging
            raise
        except Exception:
            record_auth_attempt("error")
            raise
    
    def verify_token(self, token: str) -> dict:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise UnauthorizedError("Invalid token")
            return payload
        except JWTError:
            raise UnauthorizedError("Invalid token")
    
    def refresh_access_token(self, token: str) -> dict:
        """Refresh an access token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            
            if user_id is None or email is None:
                raise UnauthorizedError("Invalid token")
            
            # Create new access token
            new_access_token = self._create_access_token({"sub": user_id, "email": email})
            
            return {
                "access_token": new_access_token,
                "token_type": "bearer",
                "user_id": user_id,
                "email": email,
                "expires_at": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            }
        except JWTError:
            raise UnauthorizedError("Invalid or expired token")

    def _create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt 