from app.db.base import SessionLocal

def get_db():
    """
    Dependency to get database session that ensures the session
    is always properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()