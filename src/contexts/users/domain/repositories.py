from abc import ABC, abstractmethod
from typing import Optional, List
from src.contexts.users.domain.entities import User


class UserRepository(ABC):
    """Abstract repository for User entities."""
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a user entity."""
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by ID."""
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email."""
        pass
    
    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username."""
        pass
    
    @abstractmethod
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Find all users with pagination."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Delete a user by ID."""
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Check if a user exists by email."""
        pass
    
    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        """Check if a user exists by username."""
        pass 