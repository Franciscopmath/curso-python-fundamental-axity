"""
Router de autenticación.

Maneja registro de usuarios y autenticación con JWT.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import Token, UserCreate, UserResponse
from app.utils.security import create_access_token, get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario.

    Args:
        user_data: Datos del usuario (username, email, password)
        db: Sesión de base de datos

    Returns:
        Usuario creado

    Raises:
        HTTPException 400: Si el username o email ya existen
    """
    # Verificar si el username ya existe
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Verificar si el email ya existe
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Crear usuario con password hasheado
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Autentica un usuario y devuelve un token JWT.

    Args:
        form_data: Formulario con username y password
        db: Sesión de base de datos

    Returns:
        Token JWT

    Raises:
        HTTPException 401: Si las credenciales son incorrectas
    """
    # Buscar usuario
    user = db.query(User).filter(User.username == form_data.username).first()

    # Verificar usuario y contraseña
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar que el usuario esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    # Crear token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Obtiene información del usuario autenticado.

    Args:
        current_user: Usuario actual (inyectado por dependencia)

    Returns:
        Información del usuario
    """
    return current_user
