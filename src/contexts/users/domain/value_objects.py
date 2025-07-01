import re
from src.shared.domain.base_value_object import BaseValueObject
from src.shared.domain.exceptions import ValidationError


class Email(BaseValueObject):
    """Email value object with validation."""
    
    def __init__(self, value: str):
        if not self._is_valid_email(value):
            raise ValidationError(f"Invalid email format: {value}")
        self.value = value.lower()
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


class Username(BaseValueObject):
    """Username value object with validation."""
    
    def __init__(self, value: str):
        if not self._is_valid_username(value):
            raise ValidationError(f"Invalid username: {value}")
        self.value = value
    
    @staticmethod
    def _is_valid_username(username: str) -> bool:
        """Validate username format."""
        if not username or len(username) < 3 or len(username) > 50:
            return False
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False
        return True


class FullName(BaseValueObject):
    """Full name value object."""
    
    def __init__(self, first_name: str, last_name: str):
        if not first_name or not first_name.strip():
            raise ValidationError("First name cannot be empty")
        if not last_name or not last_name.strip():
            raise ValidationError("Last name cannot be empty")
        
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
    
    @property
    def full_name(self) -> str:
        """Get full name as a single string."""
        return f"{self.first_name} {self.last_name}"


class HashedPassword(BaseValueObject):
    """Hashed password value object."""
    
    def __init__(self, hashed_value: str):
        if not hashed_value:
            raise ValidationError("Hashed password cannot be empty")
        self.hashed_value = hashed_value 