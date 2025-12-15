from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import Config
import logging

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(Config.DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """Dependency function to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database and create tables"""
    try:
        # Import models here to avoid circular import
        from .models import ChatLog

        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        # Create indexes if needed
        # This would be where we add any specific indexes for performance
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise