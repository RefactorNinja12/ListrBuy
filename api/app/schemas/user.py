"""import pydantic basemodel"""

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    """Create request."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserNewPassword(BaseModel): 
    new_password: str
    old_password: str


class UserPassword(BaseModel):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
