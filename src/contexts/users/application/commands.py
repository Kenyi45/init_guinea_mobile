from typing import Optional
from src.shared.application.command import Command


class CreateUserCommand(Command):
    """Command to create a new user."""
    
    email: str
    username: str
    first_name: str
    last_name: str
    password: str


class UpdateUserCommand(Command):
    """Command to update user information."""
    
    user_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class DeactivateUserCommand(Command):
    """Command to deactivate a user."""
    
    user_id: str


class ActivateUserCommand(Command):
    """Command to activate a user."""
    
    user_id: str 