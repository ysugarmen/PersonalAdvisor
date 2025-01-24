"""
This package contains all SQLAlchemy models for the application.
Import models here to make them available for usage elsewhere in the app.
"""

from app.config import Base
from app.models.user import User
from app.models.advice import Advice

__all__ = ["Base", "User", "Advice"]
