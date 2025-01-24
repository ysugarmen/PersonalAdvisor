from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.routers import user, home
import logging
from logging.handlers import RotatingFileHandler

# Logging Setup
logger = logging.getLogger("PersonalAdvisor")
logger.setLevel(logging.INFO)

# Create file handler
file_handler = RotatingFileHandler(
    "app.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)


app = FastAPI(
    title="Personal Advisor",
    description="Personal Advisor API",
    version="1.0.0",
    contact={
        "name": "Yonatan Sugarmem",
        "email": "sugaryoni3@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates_dir = Path("frontend/templates")

# Add routers with tags
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(home.router, tags=["home"])


# Middleware for logging requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(
        f"Response status: {response.status_code} {response.body if hasattr(response, 'body') else ''}"
    )
    return response


# Routes
@app.get("/")
def root_redirect() -> dict:
    """
    Root endpoint returning a basic redirect message.

    Returns:
        dict: A message indicating redirection
    """
    logger.info("Root endpoint accessed")
    return {"message": "Redirecting to /"}


@app.get("/login", response_class=HTMLResponse)
def serve_login() -> HTMLResponse:
    """
    Serve the login HTML page.

    Returns:
        HTMLResponse: Login page HTML content
    """
    logger.info("Login page requested")
    try:
        with open(templates_dir / "login.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        logger.exception("Login template not found")
        return HTMLResponse(content="<h1>Login Page Unavailable</h1>", status_code=404)


@app.get("/register", response_class=HTMLResponse)
def serve_register() -> HTMLResponse:
    """
    Serve the user registration HTML page.

    Returns:
        HTMLResponse: Registration page HTML content
    """
    logger.info("Registration page requested")
    try:
        with open(templates_dir / "register.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        logger.exception("Register template not found")
        return HTMLResponse(
            content="<h1>Registration Page Unavailable</h1>", status_code=404
        )
