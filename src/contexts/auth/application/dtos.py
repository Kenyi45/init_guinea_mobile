from datetime import datetime
from pydantic import BaseModel


class LoginDto(BaseModel):
    """DTO for user login."""
    
    email: str
    password: str


class TokenDto(BaseModel):
    """DTO for authentication token response."""
    
    access_token: str
    token_type: str
    user_id: str
    email: str
    expires_at: datetime 