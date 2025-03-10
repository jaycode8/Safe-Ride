import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

from app.db.base import Base

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    """Database model for users"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    children = relationship("Student", back_populates="parent", cascade="all, delete-orphan", lazy="joined")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<User {self.email}>"