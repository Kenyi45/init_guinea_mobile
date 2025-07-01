from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserDto(BaseModel):
    """Data Transfer Object for User."""
    
    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CreateUserDto(BaseModel):
    """DTO for creating a user."""
    
    email: str
    username: str
    first_name: str
    last_name: str
    password: str


class UpdateUserDto(BaseModel):
    """DTO for updating a user."""
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserListDto(BaseModel):
    """DTO for user list response."""
    
    users: list[UserDto]
    total: int
    limit: int
    offset: int 