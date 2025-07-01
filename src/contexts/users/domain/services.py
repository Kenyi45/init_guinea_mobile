from passlib.context import CryptContext
from src.shared.domain.exceptions import ValidationError


class PasswordService:
    """Domain service for password operations."""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        """Hash a password."""
        if not self._is_valid_password(password):
            raise ValidationError("Password does not meet requirements")
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def _is_valid_password(password: str) -> bool:
        """Validate password requirements."""
        if not password or len(password) < 8:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.islower() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        return True 