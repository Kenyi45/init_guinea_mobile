from typing import Optional
from src.shared.application.query import Query


class GetUserByIdQuery(Query):
    """Query to get a user by ID."""
    
    user_id: str


class GetUserByEmailQuery(Query):
    """Query to get a user by email."""
    
    email: str


class GetUserByUsernameQuery(Query):
    """Query to get a user by username."""
    
    username: str


class GetUsersQuery(Query):
    """Query to get all users with pagination."""
    
    limit: int = 100
    offset: int = 0 