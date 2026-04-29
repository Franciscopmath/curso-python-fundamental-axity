"""
Tests para las operaciones CRUD usando SQLite en memoria.

Este módulo prueba todas las operaciones CRUD de User, Order y OrderItem
utilizando una base de datos SQLite en memoria.
"""

from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import crud
from models import Base


@pytest.fixture
def engine():
    """Crea un motor SQLite en memoria."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Crea una sesión de base de datos para cada test."""
    with Session(engine) as session:
        yield session
        session.rollback()


# ============================================================================
# Tests para User CRUD
# ============================================================================


def test_create_user(session):
    """Prueba creación de usuario."""
    user = crud.create_user(
        session,
        username="johndoe",
        email="john@example.com",
        full_name="John Doe",
    )

    assert user.id is not None
    assert user.username == "johndoe"
    assert user.email == "john@example.com"
    assert user.full_name == "John Doe"
    assert user.created_at is not None


def test_get_user_by_id(session):
    """Prueba obtener usuario por ID."""
    user = crud.create_user(
        session, username="jane", email="jane@example.com", full_name="Jane Smith"
    )

    found = crud.get_user_by_id(session, user.id)
    assert found is not None
    assert found.username == "jane"

    not_found = crud.get_user_by_id(session, 9999)
    assert not_found is None


def test_get_user_by_username(session):
    """Prueba obtener usuario por username."""
    crud.create_user(
        session, username="alice", email="alice@example.com", full_name="Alice Wonder"
    )

    found = crud.get_user_by_username(session, "alice")
    assert found is not None
    assert found.email == "alice@example.com"

    not_found = crud.get_user_by_username(session, "nonexistent")
    assert not_found is None


def test_get_all_users(session):
    """Prueba obtener todos los usuarios."""
    crud.create_user(session, "user1", "user1@example.com", "User One")
    crud.create_user(session, "user2", "user2@example.com", "User Two")
    crud.create_user(session, "user3", "user3@example.com", "User Three")

    users = crud.get_all_users(session)
    assert len(users) == 3


def test_update_user(session):
    """Prueba actualización de usuario."""
    user = crud.create_user(
        session, username="bob", email="bob@example.com", full_name="Bob Builder"
    )

    updated = crud.update_user(
        session, user.id, email="bob.builder@example.com", full_name="Robert Builder"
    )

    assert updated is not None
    assert updated.email == "bob.builder@example.com"
    assert updated.full_name == "Robert Builder"
    assert updated.username == "bob"  # No cambió


def test_delete_user(session):
    """Prueba eliminación de usuario."""
    user = crud.create_user(
        session, username="charlie", email="charlie@example.com", full_name="Charlie"
    )

    assert crud.delete_user(session, user.id) is True
    assert crud.get_user_by_id(session, user.id) is None
    assert crud.delete_user(session, 9999) is False


# ============================================================================
# Tests para Order CRUD
# ============================================================================


def test_create_order(session):
    """Prueba creación de pedido."""
    user = crud.create_user(session, "buyer", "buyer@example.com", "Buyer One")
    order = crud.create_order(session, user.id)

    assert order is not None
    assert order.id is not None
    assert order.user_id == user.id
    assert order.status == "pending"
    assert order.total == Decimal("0.00")


def test_create_order_invalid_user(session):
    """Prueba creación de pedido con usuario inexistente."""
    order = crud.create_order(session, 9999)
    assert order is None


def test_get_order_by_id(session):
    """Prueba obtener pedido por ID."""
    user = crud.create_user(session, "buyer2", "buyer2@example.com", "Buyer Two")
    order = crud.create_order(session, user.id)

    found = crud.get_order_by_id(session, order.id)
    assert found is not None
    assert found.user_id == user.id


def test_get_orders_by_user(session):
    """Prueba obtener pedidos de un usuario."""
    user = crud.create_user(session, "buyer3", "buyer3@example.com", "Buyer Three")
    crud.create_order(session, user.id)
    crud.create_order(session, user.id)
    crud.create_order(session, user.id)

    orders = crud.get_orders_by_user(session, user.id)
    assert len(orders) == 3


def test_update_order_status(session):
    """Prueba actualización de estado de pedido."""
    user = crud.create_user(session, "buyer4", "buyer4@example.com", "Buyer Four")
    order = crud.create_order(session, user.id)

    updated = crud.update_order_status(session, order.id, "processing")
    assert updated is not None
    assert updated.status == "processing"


def test_delete_order(session):
    """Prueba eliminación de pedido."""
    user = crud.create_user(session, "buyer5", "buyer5@example.com", "Buyer Five")
    order = crud.create_order(session, user.id)

    assert crud.delete_order(session, order.id) is True
    assert crud.get_order_by_id(session, order.id) is None


# ============================================================================
# Tests para OrderItem CRUD
# ============================================================================


def test_add_item_to_order(session):
    """Prueba agregar item a pedido."""
    user = crud.create_user(session, "buyer6", "buyer6@example.com", "Buyer Six")
    order = crud.create_order(session, user.id)

    item = crud.add_item_to_order(
        session,
        order.id,
        product_name="Laptop",
        quantity=2,
        unit_price=Decimal("999.99"),
    )

    assert item is not None
    assert item.product_name == "Laptop"
    assert item.quantity == 2
    assert item.unit_price == Decimal("999.99")
    assert item.subtotal == Decimal("1999.98")


def test_add_item_to_order_updates_total(session):
    """Prueba que agregar item actualiza el total del pedido."""
    user = crud.create_user(session, "buyer7", "buyer7@example.com", "Buyer Seven")
    order = crud.create_order(session, user.id)

    crud.add_item_to_order(session, order.id, "Mouse", 3, Decimal("25.50"))

    order_updated = crud.get_order_by_id(session, order.id)
    assert order_updated.total == Decimal("76.50")


def test_get_items_by_order(session):
    """Prueba obtener items de un pedido."""
    user = crud.create_user(session, "buyer8", "buyer8@example.com", "Buyer Eight")
    order = crud.create_order(session, user.id)

    crud.add_item_to_order(session, order.id, "Item1", 1, Decimal("10.00"))
    crud.add_item_to_order(session, order.id, "Item2", 2, Decimal("20.00"))

    items = crud.get_items_by_order(session, order.id)
    assert len(items) == 2


def test_update_item_quantity(session):
    """Prueba actualización de cantidad de item."""
    user = crud.create_user(session, "buyer9", "buyer9@example.com", "Buyer Nine")
    order = crud.create_order(session, user.id)
    item = crud.add_item_to_order(session, order.id, "Keyboard", 1, Decimal("75.00"))

    updated = crud.update_item_quantity(session, item.id, 3)
    assert updated is not None
    assert updated.quantity == 3
    assert updated.subtotal == Decimal("225.00")

    # Verificar que el total del pedido se actualizó
    order_updated = crud.get_order_by_id(session, order.id)
    assert order_updated.total == Decimal("225.00")


def test_delete_item(session):
    """Prueba eliminación de item."""
    user = crud.create_user(session, "buyer10", "buyer10@example.com", "Buyer Ten")
    order = crud.create_order(session, user.id)
    item = crud.add_item_to_order(session, order.id, "Monitor", 1, Decimal("300.00"))

    assert crud.delete_item(session, item.id) is True
    assert crud.get_item_by_id(session, item.id) is None

    # Verificar que el total del pedido se recalculó
    order_updated = crud.get_order_by_id(session, order.id)
    assert order_updated.total == Decimal("0.00")


# ============================================================================
# Tests de integración
# ============================================================================


def test_complete_order_workflow(session):
    """Prueba flujo completo de creación de pedido con items."""
    # 1. Crear usuario
    user = crud.create_user(
        session,
        username="complete_user",
        email="complete@example.com",
        full_name="Complete User",
    )

    # 2. Crear pedido
    order = crud.create_order(session, user.id)
    assert order.total == Decimal("0.00")

    # 3. Agregar items
    crud.add_item_to_order(session, order.id, "Product A", 2, Decimal("50.00"))
    crud.add_item_to_order(session, order.id, "Product B", 1, Decimal("100.00"))
    crud.add_item_to_order(session, order.id, "Product C", 3, Decimal("25.00"))

    # 4. Verificar total
    order = crud.get_order_by_id(session, order.id)
    expected_total = Decimal("275.00")  # (2*50) + (1*100) + (3*25)
    assert order.total == expected_total

    # 5. Actualizar estado
    crud.update_order_status(session, order.id, "completed")
    order = crud.get_order_by_id(session, order.id)
    assert order.status == "completed"


def test_cascade_delete_user_deletes_orders(session):
    """Prueba que eliminar usuario elimina sus pedidos (cascade)."""
    user = crud.create_user(
        session, "cascade_user", "cascade@example.com", "Cascade User"
    )
    order1 = crud.create_order(session, user.id)
    order2 = crud.create_order(session, user.id)

    # Eliminar usuario
    crud.delete_user(session, user.id)

    # Verificar que los pedidos fueron eliminados
    assert crud.get_order_by_id(session, order1.id) is None
    assert crud.get_order_by_id(session, order2.id) is None


def test_cascade_delete_order_deletes_items(session):
    """Prueba que eliminar pedido elimina sus items (cascade)."""
    user = crud.create_user(
        session, "cascade_order", "cascade_order@example.com", "Cascade Order"
    )
    order = crud.create_order(session, user.id)
    item1 = crud.add_item_to_order(session, order.id, "Item1", 1, Decimal("10.00"))
    item2 = crud.add_item_to_order(session, order.id, "Item2", 2, Decimal("20.00"))

    # Eliminar pedido
    crud.delete_order(session, order.id)

    # Verificar que los items fueron eliminados
    assert crud.get_item_by_id(session, item1.id) is None
    assert crud.get_item_by_id(session, item2.id) is None


def test_recalculate_order_total(session):
    """Prueba recálculo manual del total de pedido."""
    user = crud.create_user(session, "recalc_user", "recalc@example.com", "Recalc User")
    order = crud.create_order(session, user.id)

    # Agregar items
    crud.add_item_to_order(session, order.id, "Item1", 5, Decimal("10.00"))
    crud.add_item_to_order(session, order.id, "Item2", 3, Decimal("15.00"))

    # Modificar total manualmente (simular inconsistencia)
    order = crud.get_order_by_id(session, order.id)
    order.total = Decimal("0.00")
    session.commit()

    # Recalcular
    recalculated = crud.recalculate_order_total(session, order.id)
    assert recalculated.total == Decimal("95.00")  # (5*10) + (3*15)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
