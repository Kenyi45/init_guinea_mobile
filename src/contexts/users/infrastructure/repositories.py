from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.contexts.users.domain.entities import User
from src.contexts.users.domain.repositories import UserRepository
from src.contexts.users.domain.value_objects import Email, Username, FullName, HashedPassword
from src.contexts.users.infrastructure.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository."""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def save(self, user: User) -> User:
        """Save a user entity."""
        user_model = await self._find_model_by_id(user.id)
        
        if user_model:
            # Update existing user
            user_model.email = user.email.value
            user_model.username = user.username.value
            user_model.first_name = user.full_name.first_name
            user_model.last_name = user.full_name.last_name
            user_model.hashed_password = user.hashed_password.hashed_value
            user_model.is_active = user.is_active
            user_model.updated_at = user.updated_at
        else:
            # Create new user
            user_model = UserModel(
                id=user.id,
                email=user.email.value,
                username=user.username.value,
                first_name=user.full_name.first_name,
                last_name=user.full_name.last_name,
                hashed_password=user.hashed_password.hashed_value,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            self.session.add(user_model)
        
        self.session.commit()
        self.session.refresh(user_model)
        
        return self._to_entity(user_model)
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by ID."""
        user_model = await self._find_model_by_id(user_id)
        if not user_model:
            return None
        return self._to_entity(user_model)
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email."""
        stmt = select(UserModel).where(UserModel.email == email.lower())
        result = self.session.execute(stmt)
        user_model = result.scalars().first()
        if not user_model:
            return None
        return self._to_entity(user_model)
    
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username."""
        stmt = select(UserModel).where(UserModel.username == username)
        result = self.session.execute(stmt)
        user_model = result.scalars().first()
        if not user_model:
            return None
        return self._to_entity(user_model)
    
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Find all users with pagination."""
        stmt = select(UserModel).offset(offset).limit(limit)
        result = self.session.execute(stmt)
        user_models = result.scalars().all()
        return [self._to_entity(model) for model in user_models]
    
    async def delete(self, user_id: str) -> bool:
        """Delete a user by ID."""
        user_model = await self._find_model_by_id(user_id)
        if not user_model:
            return False
        
        self.session.delete(user_model)
        self.session.commit()
        return True
    
    async def exists_by_email(self, email: str) -> bool:
        """Check if a user exists by email."""
        stmt = select(func.count(UserModel.id)).where(UserModel.email == email.lower())
        result = self.session.execute(stmt)
        count = result.scalar()
        return count > 0
    
    async def exists_by_username(self, username: str) -> bool:
        """Check if a user exists by username."""
        stmt = select(func.count(UserModel.id)).where(UserModel.username == username)
        result = self.session.execute(stmt)
        count = result.scalar()
        return count > 0
    
    async def _find_model_by_id(self, user_id: str) -> Optional[UserModel]:
        """Find a user model by ID."""
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = self.session.execute(stmt)
        return result.scalars().first()
    
    def _to_entity(self, model: UserModel) -> User:
        """Convert UserModel to User entity."""
        user = User(
            user_id=model.id,
            email=Email(model.email),
            username=Username(model.username),
            full_name=FullName(model.first_name, model.last_name),
            hashed_password=HashedPassword(model.hashed_password),
            is_active=model.is_active
        )
        
        # Set timestamps
        user._created_at = model.created_at
        user._updated_at = model.updated_at
        
        return user 