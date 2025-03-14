from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.services.user_service import get_users, get_user, create_user_by_admin, update_user, deactivate_user, activate_user
from app.services.student_service import get_students, get_students_by_parent
from app.utils.security import get_current_user

# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def dashboard(request: Request, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if current_user.role.value == "ADMIN":
        users = get_users(db)
        return templates.TemplateResponse(
            "dashboard.html", 
            {
                "request": request, 
                "current_user": current_user,
                "users": users,
            }
        )
    else:
        students = get_students_by_parent(db, current_user.id)
        return templates.TemplateResponse(
            "parents_dashboard.html", 
            {
                "request": request,
                "current_user": current_user,
                "children": students
            }
        )

@router.get("/user/create")
async def user_create_form(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse(
        "user_form.html", 
        {
            "request": request,
            "current_user": current_user,
            "roles": UserRole,
            "is_new": True
        }
    )

@router.post("/user/create")
async def create_user(request: Request, email: str = Form(...), password: str = Form(...), first_name: Optional[str] = Form(None), last_name: Optional[str] = Form(None), db: Session = Depends(get_db)):
    user_data = UserCreate(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    
    create_user_by_admin(db, user_data)
    
    return RedirectResponse(
        url="/dashboard", 
        status_code=status.HTTP_303_SEE_OTHER
    )

@router.get("/user/{user_id}/edit")
async def user_edit_form(request: Request, user_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, user_id)
    
    return templates.TemplateResponse(
        "user_form.html", 
        {
            "request": request,
            "current_user": current_user,
            "user": user,
            "roles": UserRole,
            "is_new": False
        }
    )

@router.post("/user/{user_id}/edit")
async def edit_user(request: Request, user_id: int, email: str = Form(...), first_name: Optional[str] = Form(None), last_name: Optional[str] = Form(None), db: Session = Depends(get_db)):
    user_data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }
    
    update_user(db, user_id, user_data)
    
    return RedirectResponse(
        url="/dashboard", 
        status_code=status.HTTP_303_SEE_OTHER
    )

@router.post("/user/{user_id}/deactivate")
async def deactivate_user_route(user_id: int, db: Session = Depends(get_db)):
    deactivate_user(db, user_id)
    
    return RedirectResponse(
        url="/dashboard", 
        status_code=status.HTTP_303_SEE_OTHER
    )

@router.post("/user/{user_id}/activate")
async def activate_user_route(user_id: int, db: Session = Depends(get_db)):
    activate_user(db, user_id)
    
    return RedirectResponse(
        url="/dashboard",
        status_code=status.HTTP_303_SEE_OTHER
    )
