"""
Utilidades de seguridad para autenticación y manejo de passwords.
"""

from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# Contexto de encriptación de passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash.

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada

    Returns:
        True si coinciden, False en caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash de la contraseña.

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash de la contraseña
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Crea un token JWT.

    Args:
        data: Datos a incluir en el token (ej: {"sub": "username"})
        expires_delta: Tiempo de expiración opcional

    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> str | None:
    """
    Verifica y decodifica un token JWT.

    Args:
        token: Token JWT

    Returns:
        Username si el token es válido, None en caso contrario
    """
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str | None = payload.get("sub")
        return username
    except JWTError:
        return None
