from pydantic import BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, description="The username of the user"
    )
    email: EmailStr = Field(..., description="The email of the user")
    password: str = Field(
        ..., min_length=8, max_length=255, description="The password of the user"
    )

    @validator("password")
    def validate_password(cls, value: str) -> str:
        """
        Ensure password meets minimum security requirements.
        """
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        return value


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="The user's email address.")
    password: str = Field(..., description="The user's password.")


class UserResponse(BaseModel):
    id: int = Field(..., description="The user's unique identifier.")
    username: str = Field(..., description="The username of the user.")
    email: EmailStr = Field(..., description="The user's email address.")

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="The JWT access token.")
    token_type: str = Field(..., description="The token type (e.g., bearer).")
