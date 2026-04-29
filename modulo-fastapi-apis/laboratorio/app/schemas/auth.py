"""
Schemas Pydantic para autenticación.
"""

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema para crear un usuario."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class UserResponse(BaseModel):
    """Schema para respuesta de usuario (sin password)."""

    id: int
    username: str
    email: str
    is_active: bool

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Schema para respuesta de token JWT."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema para datos dentro del token."""

    username: str | None = None
