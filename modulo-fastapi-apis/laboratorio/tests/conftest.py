"""
Configuración de pytest y fixtures compartidos.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.utils.security import get_password_hash

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_db():
    """
    Crea una base de datos de prueba en memoria.

    Yields:
        Sesión de base de datos para tests
    """
    # Crear tablas
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Limpiar tablas
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db: Session):
    """
    Crea un cliente de prueba de FastAPI con base de datos temporal.

    Args:
        test_db: Sesión de base de datos de prueba

    Yields:
        TestClient configurado con base de datos de prueba
    """

    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(test_db: Session):
    """
    Crea un usuario de prueba en la base de datos.

    Args:
        test_db: Sesión de base de datos de prueba

    Returns:
        Usuario de prueba creado
    """
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        is_active=True,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def auth_headers(client: TestClient, test_user: User):
    """
    Obtiene headers de autenticación para requests.

    Args:
        client: Cliente de prueba
        test_user: Usuario de prueba

    Returns:
        Dict con header Authorization
    """
    response = client.post(
        "/auth/token", data={"username": "testuser", "password": "testpassword123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
