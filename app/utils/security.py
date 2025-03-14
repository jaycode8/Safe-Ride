from fastapi import status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from app.config import settings
from fastapi.responses import RedirectResponse
from app.models.user import User
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db

SECRET_KEY = "your_secret_key_here"  # Use the same secret key
ALGORITHM = "HS256"
# Password hashing utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that plain_password matches hashed_password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash from plain password"""
    return pwd_context.hash(password)

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get the current logged-in user from the session token"""
    token = request.cookies.get("session")

    if not token:
        # return RedirectResponse(
        #     url="/login", 
        #     status_code=status.HTTP_401_UNAUTHORIZED
        # )
        raise HTTPException(
            status_code=401, detail="Not authenticated"
        )
        # return RedirectResponse(url="/login")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        if not email:
            return RedirectResponse(
                url="/login", 
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        current_user = get_user_by_email(db, email)
        
        return current_user

    except JWTError:
        return RedirectResponse(
            url="/login", 
            status_code=status.HTTP_401_UNAUTHORIZED
        )