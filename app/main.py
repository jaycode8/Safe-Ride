import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.config import settings
from app.db.base import Base, engine
from app.db.session import get_db
from app.services.auth_service import create_admin_user
from app.controllers import auth_controller, user_controller, student_controller, detection_controller

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(student_controller.router)
app.include_router(detection_controller.router)

# Initialize templates
templates = Jinja2Templates(directory="app/templates")

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 401:
        return RedirectResponse(url="/login")
    return RedirectResponse(url="/error")

@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup.
    Creates admin user if one doesn't exist.
    """
    logger.info("Starting up FastAPI application...")
    
    try:
        # Get DB session
        db = next(get_db())
        
        # Create admin user
        admin = create_admin_user(db)
        logger.info(f"Admin user ensured: {admin.email}")
        
    except Exception as e:
        logger.error(f"Startup error: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)