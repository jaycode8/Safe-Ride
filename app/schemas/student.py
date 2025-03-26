from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class StudentBase(BaseModel):
    """Base schema for student data"""
    adm_no: str
    
class StudentCreate(StudentBase):
    """Schema for creating a new Student"""
    full_name: str
    level: str
    parent_id: Optional[int] = None

class StudentUpdate(BaseModel):
    """Schema for updating Student information"""
    full_name: Optional[str] = None
    adm_no: Optional[str] = None
    level: Optional[str] = None
    parent_id: Optional[int] = None
    left_at: Optional[datetime] = None
    
class StudentInDB(StudentBase):
    """Schema for Student information retrieved from the database"""
    id: int
    full_name: Optional[str] = None
    adm_no: Optional[str] = None
    level: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class ConfigDict:
        from_attributes = True

class Student(StudentInDB):
    """Schema for public Student information"""
    pass
