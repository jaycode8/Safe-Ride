from datetime import timedelta, datetime
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.utils.security import verify_password, get_password_hash
from app.config import settings

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user with email and password
        
    Returns:
        User object if authentication succeeds, None otherwise
    """
    user = db.query(User).filter(User.email == email).first()
    
    if user and verify_password(password, user.hashed_password):
        return user
    
    return None

def create_session_token(data: dict, expires_delta: timedelta):
    """Create a JWT session token with an expiry time"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_user(db: Session, user_data: UserCreate, is_admin: bool = False) -> User:
    """
    Create a new user in the database
    
    Returns:
        Created user object
    """
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=UserRole.ADMIN if is_admin else user_data.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def create_admin_user(db: Session) -> User:
    """
    Create admin user if one doesn't exist
    
    Returns:
        Created or existing admin user
    """
    # Check if any admin user exists
    admin_user = db.query(User).filter(User.role == UserRole.ADMIN).first()
    
    if admin_user:
        return admin_user
    
    # Create admin user
    admin_data = UserCreate(
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
        first_name="Admin",
        last_name="User",
        role=UserRole.ADMIN
    )
    
    return create_user(db, admin_data, is_admin=True)
