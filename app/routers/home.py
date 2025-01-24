from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.config import get_db, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from app.models.user import User
import logging

# Router setup
router = APIRouter()

# Template directory setup
templates = Jinja2Templates(directory="frontend/templates")

# Logger setup
logger = logging.getLogger("HomeRouter")


@router.get("/", response_class=HTMLResponse)
def redirect_to_login():
    """Redirect the root route to the login page."""
    return RedirectResponse("/login")


@router.get("/home", response_class=HTMLResponse)
def home(request: Request, token: str, db: Session = Depends(get_db)):
    """
    Render the home page for the specified user.

    Args:
        request (Request): The HTTP request object.
        user_id (int, optional): The ID of the user. Defaults to None.
        db (Session): The database session dependency.

    Returns:
        HTMLResponse: The rendered home page.

    Raises:
        HTTPException: If the user is not found.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        logger.warning("Invalid or missing token")
        return RedirectResponse("/login")

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        logger.error(f"User not found for token: {user_id}")
        return RedirectResponse("/login")

    logger.info(f"Rendering home page for user: {db_user.username}")
    return templates.TemplateResponse(
        "home.html", {"request": request, "username": db_user.username}
    )
