from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate

def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
    """
    Get a list of students filtered by parent_id
    """
    return db.query(Student).offset(skip).limit(limit).all()

def get_students_by_parent(db: Session, parent_id: int, skip: int = 0, limit: int = 100) -> List[Student]:
    """
    Get a list of students filtered by parent_id
    """
    return db.query(Student).filter(Student.parent_id == parent_id).offset(skip).limit(limit).all()


def get_student(db: Session, stud_id: int) -> Optional[Student]:
    """
    Get a student by ID
    """
    return db.query(Student).filter(Student.id == stud_id).first()

def get_student_by_adm(db: Session, adm_no: str) -> Optional[Student]:
    """
    Get a sudent by adm
    """
    return db.query(Student).filter(Student.adm_no == adm_no).first()

def update_student(db: Session, stud_id: int, stud_data: StudentUpdate) -> Student:
    """
    Update a student's information
    """
    stud = get_student(db, stud_id)
    
    if not stud:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="student not found"
        )
    
    update_data = stud_data if isinstance(stud_data, dict) else stud_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(stud, key, value)
    
    db.commit()
    db.refresh(stud)
    
    return stud

def create_stud_by_admin(db: Session, stud_data: StudentCreate) -> Student:
    """
    Create a new student by admin
    """
    existing_stud = get_student_by_adm(db, stud_data.adm_no)
    if existing_stud:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admission number already registered"
        )

    parent = None
    if stud_data.parent_id:
        parent = db.query(User).filter(User.id == stud_data.parent_id).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent not found"
            )
    
    db_stud = Student(
        adm_no=stud_data.adm_no,
        full_name=stud_data.full_name,
        level=stud_data.level,
        parent_id=stud_data.parent_id
    )
    print(db_stud)
    
    db.add(db_stud)
    db.commit()
    db.refresh(db_stud)

    if parent:
        parent.children.append(db_stud)
        db.add(parent)
        db.commit()
        db.refresh(parent)
    
    return db_stud