from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import get_password_hash

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Get a list of users
    """
    return db.query(User).offset(skip).limit(limit).all()

def get_parents(db: Session) -> List[User]:
    """
    Get a list of parents
    """
    return db.query(User).filter(User.role == "user").all()

def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Get a user by ID
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email
    """
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    """
    Update a user's information
    """
    user = get_user(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_data if isinstance(user_data, dict) else user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    return user

def deactivate_user(db: Session, user_id: int) -> User:
    """
    Deactivate a user account
    """
    user = get_user(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    db.commit()
    db.refresh(user)
    
    return user

def activate_user(db: Session, user_id: int) -> User:
    """
    Activate a user account
    """
    user = get_user(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    db.commit()
    db.refresh(user)
    
    return user


def create_user_by_admin(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user by admin
    """
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user