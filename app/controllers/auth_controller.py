from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserLogin
# from app.services.auth_service import authenticate_user, create_session_token
from app.utils.security import verify_password
from app.config import settings

# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
async def login_page(request: Request):
    """Render the login page"""
    return templates.TemplateResponse("login.html", {"request": request})

# @router.post("/login")
# async def login(
#     response: Response,
#     request: Request,
#     form_data: UserLogin, 
#     db: Session = Depends(get_db)
# ):
#     """Authenticate user and set session cookie"""
#     # Authenticate user
#     user = authenticate_user(db, form_data.email, form_data.password)
    
#     if not user:
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     # Create session token
#     # access_token = create_session_token(user)
#     access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(hours=1))
    
#     # Set session cookie
#     response = RedirectResponse(url="/dashboard", status_code=303)
#     # response = HTMLResponse(data="mambo")
#     response.set_cookie(
#         key="session",
#         value=access_token,
#         httponly=True,
#         secure=False,  # Set to True in production with HTTPS
#         samesite="lax",
#         max_age=3600
#     )
    
#     return response

@router.get("/logout")
async def logout():
    """Handle user logout by clearing session cookie"""
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="session")
    
    return response