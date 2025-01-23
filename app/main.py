from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.routers import user, home

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates_dir = Path("frontend/templates")

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(home.router, tags=["home"])


# Routes
@app.get("/")
def root_redirect():
    return {"message": "Redirecting to /"}


@app.get("/login", response_class=HTMLResponse)
def serve_login():
    with open(templates_dir / "login.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/register", response_class=HTMLResponse)
def serve_register():
    with open(templates_dir / "register.html", "r") as f:
        return HTMLResponse(content=f.read())
