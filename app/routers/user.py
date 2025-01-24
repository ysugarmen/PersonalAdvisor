from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.config import get_db, SECRET_KEY, ALGORITHM
from app.models.user import User
from passlib.context import CryptContext
from jose import jwt
import logging

# Logger setup
logger = logging.getLogger("UserRouter")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Router setup
router = APIRouter()

# Templates setup
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/login", response_class=HTMLResponse)
def serve_login(request: Request):
    """Serve the login page."""
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Authenticate user and redirect to the home page if successful."""
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not pwd_context.verify(password, db_user.hashed_password):
        logger.warning(f"Login failed for email: {email}")
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid email or password"},
        )

    access_token = jwt.encode(
        {"sub": str(db_user.id)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    logger.info(f"Login successful for user: {db_user.username}")
    response = RedirectResponse("/home", status_code=303)
    response.set_cookie(
        key="Authorization", value=f"Bearer {access_token}", httponly=True
    )
    return response


@router.get("/register", response_class=HTMLResponse)
def serve_register(request: Request):
    """Serve the registration page."""
    return templates.TemplateResponse(
        "register.html", {"request": request, "error": None}
    )


@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Register a new user and redirect to the home page if successful."""
    if db.query(User).filter(User.email == email).first():
        logger.warning(f"Registration failed: Email already registered ({email})")
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Email already registered"},
        )

    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"User registered successfully: {username}")
    access_token = jwt.encode(
        {"sub": str(new_user.id)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    response = RedirectResponse("/home", status_code=303)
    response.set_cookie(
        key="Authorization", value=f"Bearer {access_token}", httponly=True
    )
    return response
