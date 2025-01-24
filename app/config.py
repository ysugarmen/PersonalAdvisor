from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Logger setup
logger = logging.getLogger("ConfigLogger")
logger.setLevel(logging.INFO)

# Database setup
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://yonatansugarmen:your_password@localhost:5432/personal_advisor",
)
if not DATABASE_URL:
    logger.error("DATABASE_URL is not set. Please check your .env file.")
else:
    logger.info("Database URL successfully loaded.")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT setup
SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
if SECRET_KEY == "mysecretkey":
    logger.warning("Using default SECRET_KEY. Set a secure key in your .env file.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# Dependency for database session
def get_db():
    """
    Dependency that provides a SQLAlchemy session.
    Ensures proper session handling for database operations.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
