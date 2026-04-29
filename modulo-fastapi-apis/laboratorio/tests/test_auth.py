"""
Tests de autenticación y registro de usuarios.
"""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test del endpoint raíz."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check(client: TestClient):
    """Test del endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_register_user_success(client: TestClient):
    """Test de registro exitoso de usuario."""
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # Password no debe exponerse


def test_register_duplicate_username(client: TestClient, test_user):
    """Test de registro con username duplicado."""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",  # Ya existe
            "email": "different@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_duplicate_email(client: TestClient, test_user):
    """Test de registro con email duplicado."""
    response = client.post(
        "/auth/register",
        json={
            "username": "differentuser",
            "email": "test@example.com",  # Ya existe
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_invalid_email(client: TestClient):
    """Test de registro con email inválido."""
    response = client.post(
        "/auth/register",
        json={"username": "user", "email": "not-an-email", "password": "password123"},
    )
    assert response.status_code == 422  # Validation error


def test_register_short_password(client: TestClient):
    """Test de registro con password muy corto."""
    response = client.post(
        "/auth/register",
        json={"username": "user", "email": "user@example.com", "password": "short"},
    )
    assert response.status_code == 422  # Validation error


def test_login_success(client: TestClient, test_user):
    """Test de login exitoso."""
    response = client.post(
        "/auth/token", data={"username": "testuser", "password": "testpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, test_user):
    """Test de login con contraseña incorrecta."""
    response = client.post(
        "/auth/token", data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user(client: TestClient):
    """Test de login con usuario que no existe."""
    response = client.post(
        "/auth/token",
        data={"username": "nonexistent", "password": "somepassword"},
    )
    assert response.status_code == 401


def test_get_current_user(client: TestClient, auth_headers):
    """Test de obtener información del usuario autenticado."""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data


def test_get_current_user_without_token(client: TestClient):
    """Test de acceder a /me sin token."""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_get_current_user_invalid_token(client: TestClient):
    """Test de acceder a /me con token inválido."""
    response = client.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
