"""
Tests de CRUD de pedidos (Orders).
"""

from decimal import Decimal

from fastapi.testclient import TestClient


def test_create_order_success(client: TestClient, auth_headers):
    """Test de creación exitosa de pedido."""
    response = client.post(
        "/orders/",
        json={"product_name": "Laptop", "quantity": 2, "unit_price": 999.99},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == "Laptop"
    assert data["quantity"] == 2
    assert float(data["unit_price"]) == 999.99
    assert float(data["total"]) == 1999.98
    assert data["status"] == "pending"
    assert "id" in data
    assert "user_id" in data


def test_create_order_without_auth(client: TestClient):
    """Test de crear pedido sin autenticación."""
    response = client.post(
        "/orders/",
        json={"product_name": "Mouse", "quantity": 1, "unit_price": 25.50},
    )
    assert response.status_code == 401


def test_create_order_invalid_quantity(client: TestClient, auth_headers):
    """Test de crear pedido con cantidad inválida (0 o negativa)."""
    response = client.post(
        "/orders/",
        json={"product_name": "Product", "quantity": 0, "unit_price": 10.00},
        headers=auth_headers,
    )
    assert response.status_code == 422  # Validation error

    response = client.post(
        "/orders/",
        json={"product_name": "Product", "quantity": -5, "unit_price": 10.00},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_create_order_invalid_price(client: TestClient, auth_headers):
    """Test de crear pedido con precio inválido."""
    response = client.post(
        "/orders/",
        json={"product_name": "Product", "quantity": 1, "unit_price": -10.00},
        headers=auth_headers,
    )
    assert response.status_code == 422  # Validation error


def test_create_order_product_name_whitespace(client: TestClient, auth_headers):
    """Test de crear pedido con espacios al inicio/final del nombre."""
    response = client.post(
        "/orders/",
        json={"product_name": "  Product  ", "quantity": 1, "unit_price": 10.00},
        headers=auth_headers,
    )
    assert response.status_code == 422  # Validation error


def test_list_orders_empty(client: TestClient, auth_headers):
    """Test de listar pedidos cuando no hay ninguno."""
    response = client.get("/orders/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_list_orders_with_data(client: TestClient, auth_headers):
    """Test de listar pedidos con datos."""
    # Crear varios pedidos
    client.post(
        "/orders/",
        json={"product_name": "Product 1", "quantity": 1, "unit_price": 10.00},
        headers=auth_headers,
    )
    client.post(
        "/orders/",
        json={"product_name": "Product 2", "quantity": 2, "unit_price": 20.00},
        headers=auth_headers,
    )

    response = client.get("/orders/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["product_name"] == "Product 1"
    assert data[1]["product_name"] == "Product 2"


def test_list_orders_pagination(client: TestClient, auth_headers):
    """Test de paginación en listado de pedidos."""
    # Crear 5 pedidos
    for i in range(5):
        client.post(
            "/orders/",
            json={"product_name": f"Product {i}", "quantity": 1, "unit_price": 10.00},
            headers=auth_headers,
        )

    # Obtener primeros 2
    response = client.get("/orders/?skip=0&limit=2", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Obtener siguientes 2
    response = client.get("/orders/?skip=2&limit=2", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_order_by_id(client: TestClient, auth_headers):
    """Test de obtener pedido por ID."""
    # Crear pedido
    create_response = client.post(
        "/orders/",
        json={"product_name": "Keyboard", "quantity": 1, "unit_price": 75.00},
        headers=auth_headers,
    )
    order_id = create_response.json()["id"]

    # Obtener pedido
    response = client.get(f"/orders/{order_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["product_name"] == "Keyboard"


def test_get_nonexistent_order(client: TestClient, auth_headers):
    """Test de obtener pedido que no existe."""
    response = client.get("/orders/9999", headers=auth_headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_order_product_name(client: TestClient, auth_headers):
    """Test de actualizar nombre de producto."""
    # Crear pedido
    create_response = client.post(
        "/orders/",
        json={"product_name": "Old Name", "quantity": 1, "unit_price": 10.00},
        headers=auth_headers,
    )
    order_id = create_response.json()["id"]

    # Actualizar
    response = client.put(
        f"/orders/{order_id}",
        json={"product_name": "New Name"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product_name"] == "New Name"
    assert data["quantity"] == 1  # No cambió


def test_update_order_quantity_recalculates_total(client: TestClient, auth_headers):
    """Test de que actualizar cantidad recalcula el total."""
    # Crear pedido
    create_response = client.post(
        "/orders/",
        json={"product_name": "Product", "quantity": 2, "unit_price": 50.00},
        headers=auth_headers,
    )
    order_id = create_response.json()["id"]
    assert float(create_response.json()["total"]) == 100.00

    # Actualizar cantidad
    response = client.put(
        f"/orders/{order_id}", json={"quantity": 5}, headers=auth_headers
    )
    assert response.status_code == 200
    assert float(response.json()["total"]) == 250.00  # 5 * 50


def test_update_order_status(client: TestClient, auth_headers):
    """Test de actualizar estado del pedido."""
    # Crear pedido
    create_response = client.post(
        "/orders/",
        json={"product_name": "Product", "quantity": 1, "unit_price": 10.00},
        headers=auth_headers,
    )
    order_id = create_response.json()["id"]

    # Actualizar estado
    response = client.put(
        f"/orders/{order_id}", json={"status": "completed"}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_update_order_invalid_status(client: TestClient, auth_headers):
    """Test de actualizar con estado inválido."""
    # Crear pedido
    create_response = client.post(
        "/orders/",
        json={"product_name": "Product", "quantity": 1, "unit_price": 10.00},
        headers=auth_headers,
    )
    order_id = create_response.json()["id"]

    # Intentar actualizar con estado inválido
    response = client.put(
        f"/orders/{order_id}", json={"status": "invalid_status"}, headers=auth_headers
    )
    assert response.status_code == 422  # Validation error


def test_delete_order(client: TestClient, auth_headers):
    """Test de eliminar pedido."""
    # Crear pedido
    create_response = client.post(
        "/orders/",
        json={"product_name": "Product", "quantity": 1, "unit_price": 10.00},
        headers=auth_headers,
    )
    order_id = create_response.json()["id"]

    # Eliminar
    response = client.delete(f"/orders/{order_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verificar que ya no existe
    response = client.get(f"/orders/{order_id}", headers=auth_headers)
    assert response.status_code == 404


def test_delete_nonexistent_order(client: TestClient, auth_headers):
    """Test de eliminar pedido que no existe."""
    response = client.delete("/orders/9999", headers=auth_headers)
    assert response.status_code == 404


def test_user_cannot_access_other_user_order(client: TestClient, test_db):
    """Test de que un usuario no puede acceder a pedidos de otro usuario."""
    from app.models.user import User
    from app.utils.security import get_password_hash

    # Crear segundo usuario
    user2 = User(
        username="user2",
        email="user2@example.com",
        hashed_password=get_password_hash("password123"),
    )
    test_db.add(user2)
    test_db.commit()

    # Login como usuario1 y crear pedido
    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)

    response1 = client.post(
        "/auth/token", data={"username": "testuser", "password": "testpassword123"}
    )
    token1 = response1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    create_response = client.post(
        "/orders/",
        json={"product_name": "Product", "quantity": 1, "unit_price": 10.00},
        headers=headers1,
    )
    order_id = create_response.json()["id"]

    # Login como usuario2 e intentar acceder al pedido de usuario1
    response2 = client.post(
        "/auth/token", data={"username": "user2", "password": "password123"}
    )
    token2 = response2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    response = client.get(f"/orders/{order_id}", headers=headers2)
    assert response.status_code == 403  # Forbidden
    assert "not authorized" in response.json()["detail"].lower()
