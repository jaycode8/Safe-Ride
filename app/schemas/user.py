from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    """Base schema for user data"""
    email: EmailStr
    
class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    @field_validator('password')
    def password_must_be_strong(cls, v):
        """Validate password strength"""
        if len(v) < 5:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    
class UserInDB(UserBase):
    """Schema for user information retrieved from the database"""
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime
    
    class ConfigDict:
        from_attributes = True

class User(UserInDB):
    """Schema for public user information"""
    pass

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for token payload data"""
    email: Optional[str] = None
    role: Optional[str] = None