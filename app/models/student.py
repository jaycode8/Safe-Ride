import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base

class Student(Base):
    """Database model for students"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), unique=True, index=True, nullable=False)
    level = Column(String(255), nullable=False)
    adm_no = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    parent = relationship("User", back_populates="children", lazy="joined")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<User {self.full_name}>"