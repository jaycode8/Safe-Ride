from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.db.session import get_db
from app.services.auth_service import authenticate_user, create_session_token
from app.config import settings

# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Secret Key and JWT Configuration
SECRET_KEY = "your_secret_key_here"  # Use a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

@router.get("/login")
async def login_page(request: Request):
    """Render the login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, response: Response, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Authenticate user and set session token"""
    user = authenticate_user(db, email, password)
    
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid email or password", "email": email},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Generate session token
    access_token = create_session_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Set session cookie
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="session",
        value=access_token,
        httponly=True,
        secure=False,  # Change to True in production (with HTTPS)
        samesite="lax",
        max_age=3600
    )
    
    return response

@router.post("/logout")
async def logout():
    """Handle user logout by clearing session cookie"""
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="session")
    return response
