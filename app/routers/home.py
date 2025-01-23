from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.config import get_db
from app.models.user import User

router = APIRouter()

templates = Jinja2Templates(directory="frontend/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, user_id: int, db: Session = Depends(get_db)):
    """Render the home page."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(
        "home.html", {"request": request, "username": db_user.username}
    )
