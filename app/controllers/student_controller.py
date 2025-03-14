from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.services.student_service import get_student, create_stud_by_admin, update_student
from app.services.user_service import get_parents
from app.utils.security import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/student/create")
async def stud_create_form(request: Request, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    parents = get_parents(db)
    return templates.TemplateResponse(
        "student_form.html", 
        {
            "request": request,
            "current_user": current_user,
            "is_new": True,
            "parents": parents
        }
    )

@router.post("/student/create")
async def create_stud(request: Request, full_name: str = Form(...), adm_no: str = Form(...), level: str = Form(...), parent_id: str = Form(...), db: Session = Depends(get_db)):
    stud_data = StudentCreate(
        full_name=full_name,
        adm_no=adm_no,
        level=level,
        parent_id=parent_id
    )
    
    create_stud_by_admin(db, stud_data)
    
    return RedirectResponse(
        url="/dashboard", 
        status_code=status.HTTP_303_SEE_OTHER
    )

@router.get("/student/{student_id}/edit")
async def student_edit_form(request: Request, student_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    student = get_student(db, student_id)
    parents = get_parents(db)
    
    return templates.TemplateResponse(
        "student_form.html", 
        {
            "request": request,
            "current_user": current_user,
            "student": student,
            "parents": parents,
            "is_new": False
        }
    )

@router.post("/student/{student_id}/edit")
async def edit_user(request: Request, student_id: int, full_name: str = Form(...), adm_no: str = Form(...), level: str = Form(...), parent_id: str = Form(...), db: Session = Depends(get_db)):
    stud_data = StudentUpdate(
        full_name=full_name,
        adm_no=adm_no,
        level=level,
        parent_id=parent_id
    )
    print(stud_data)
    update_student(db, student_id, stud_data)

    return RedirectResponse(
        url="/dashboard", 
        status_code=status.HTTP_303_SEE_OTHER
    )
