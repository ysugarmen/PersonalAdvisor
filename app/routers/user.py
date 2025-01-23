from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlalchemy.orm import Session
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, get_db
from app.models.user import User
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.schemas.user import UserCreate, UserLogin


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/signup", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and store their data in the database."""
    logging.info(f"Received signup request for user: {user}")
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        logging.error(f"Email already registered: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    logging.info("Hashed password generated")
    new_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logging.info(f"User created successfully: {new_user}")
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
    }


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a user by their ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token"""
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
