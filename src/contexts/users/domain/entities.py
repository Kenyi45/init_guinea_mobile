from typing import Optional
from src.shared.domain.base_entity import BaseEntity, DomainEvent
from src.contexts.users.domain.value_objects import Email, Username, FullName, HashedPassword


class UserCreated(DomainEvent):
    """Domain event for when a user is created."""
    
    def __init__(self, user_id: str, email: str, username: str):
        super().__init__(
            event_type="user_created",
            data={
                "user_id": user_id,
                "email": email,
                "username": username
            }
        )


class UserUpdated(DomainEvent):
    """Domain event for when a user is updated."""
    
    def __init__(self, user_id: str, changes: dict):
        super().__init__(
            event_type="user_updated",
            data={
                "user_id": user_id,
                "changes": changes
            }
        )


class User(BaseEntity):
    """User entity representing a system user."""
    
    def __init__(
        self,
        user_id: Optional[str] = None,
        email: Optional[Email] = None,
        username: Optional[Username] = None,
        full_name: Optional[FullName] = None,
        hashed_password: Optional[HashedPassword] = None,
        is_active: bool = True
    ):
        super().__init__(user_id)
        self._email = email
        self._username = username
        self._full_name = full_name
        self._hashed_password = hashed_password
        self._is_active = is_active
    
    @property
    def email(self) -> Optional[Email]:
        return self._email
    
    @property
    def username(self) -> Optional[Username]:
        return self._username
    
    @property
    def full_name(self) -> Optional[FullName]:
        return self._full_name
    
    @property
    def hashed_password(self) -> Optional[HashedPassword]:
        return self._hashed_password
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    @classmethod
    def create(
        cls,
        email: str,
        username: str,
        first_name: str,
        last_name: str,
        hashed_password: str
    ) -> "User":
        """Factory method to create a new user."""
        user = cls(
            email=Email(email),
            username=Username(username),
            full_name=FullName(first_name, last_name),
            hashed_password=HashedPassword(hashed_password),
            is_active=True
        )
        
        # Add domain event
        user.add_domain_event(UserCreated(
            user_id=user.id,
            email=email,
            username=username
        ))
        
        return user
    
    def update_profile(self, first_name: str = None, last_name: str = None) -> None:
        """Update user profile information."""
        changes = {}
        
        if first_name is not None or last_name is not None:
            current_first = self._full_name.first_name if self._full_name else ""
            current_last = self._full_name.last_name if self._full_name else ""
            
            new_first = first_name if first_name is not None else current_first
            new_last = last_name if last_name is not None else current_last
            
            self._full_name = FullName(new_first, new_last)
            changes["full_name"] = self._full_name.full_name
        
        if changes:
            self.mark_updated()
            self.add_domain_event(UserUpdated(
                user_id=self.id,
                changes=changes
            ))
    
    def deactivate(self) -> None:
        """Deactivate the user."""
        if self._is_active:
            self._is_active = False
            self.mark_updated()
            self.add_domain_event(UserUpdated(
                user_id=self.id,
                changes={"is_active": False}
            ))
    
    def activate(self) -> None:
        """Activate the user."""
        if not self._is_active:
            self._is_active = True
            self.mark_updated()
            self.add_domain_event(UserUpdated(
                user_id=self.id,
                changes={"is_active": True}
            )) 