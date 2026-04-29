"""
Operaciones CRUD para User, Order y OrderItem.

Este módulo proporciona funciones para crear, leer, actualizar y eliminar
registros de las tres entidades principales del sistema.
"""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models import Order, OrderItem, User

# ============================================================================
# CRUD para User
# ============================================================================


def create_user(session: Session, username: str, email: str, full_name: str) -> User:
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        session: Sesión de SQLAlchemy
        username: Nombre de usuario único
        email: Email único del usuario
        full_name: Nombre completo del usuario

    Returns:
        Usuario creado

    Raises:
        IntegrityError: Si el username o email ya existen
    """
    user = User(username=username, email=email, full_name=full_name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(session: Session, user_id: int) -> User | None:
    """
    Obtiene un usuario por su ID.

    Args:
        session: Sesión de SQLAlchemy
        user_id: ID del usuario

    Returns:
        Usuario encontrado o None si no existe
    """
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str) -> User | None:
    """
    Obtiene un usuario por su username.

    Args:
        session: Sesión de SQLAlchemy
        username: Nombre de usuario

    Returns:
        Usuario encontrado o None si no existe
    """
    stmt = select(User).where(User.username == username)
    return session.scalars(stmt).first()


def get_all_users(session: Session, limit: int = 100) -> list[User]:
    """
    Obtiene todos los usuarios.

    Args:
        session: Sesión de SQLAlchemy
        limit: Número máximo de usuarios a retornar

    Returns:
        Lista de usuarios
    """
    stmt = select(User).limit(limit)
    return list(session.scalars(stmt).all())


def update_user(
    session: Session,
    user_id: int,
    username: str | None = None,
    email: str | None = None,
    full_name: str | None = None,
) -> User | None:
    """
    Actualiza los datos de un usuario.

    Args:
        session: Sesión de SQLAlchemy
        user_id: ID del usuario a actualizar
        username: Nuevo username (opcional)
        email: Nuevo email (opcional)
        full_name: Nuevo nombre completo (opcional)

    Returns:
        Usuario actualizado o None si no existe
    """
    user = get_user_by_id(session, user_id)
    if not user:
        return None

    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if full_name is not None:
        user.full_name = full_name

    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    """
    Elimina un usuario y todos sus pedidos (cascade).

    Args:
        session: Sesión de SQLAlchemy
        user_id: ID del usuario a eliminar

    Returns:
        True si se eliminó, False si no existía
    """
    user = get_user_by_id(session, user_id)
    if not user:
        return False

    session.delete(user)
    session.commit()
    return True


# ============================================================================
# CRUD para Order
# ============================================================================


def create_order(
    session: Session, user_id: int, status: str = "pending"
) -> Order | None:
    """
    Crea un nuevo pedido para un usuario.

    Args:
        session: Sesión de SQLAlchemy
        user_id: ID del usuario que crea el pedido
        status: Estado inicial del pedido (default: 'pending')

    Returns:
        Pedido creado o None si el usuario no existe
    """
    user = get_user_by_id(session, user_id)
    if not user:
        return None

    order = Order(user_id=user_id, status=status, total=Decimal("0.00"))
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_order_by_id(session: Session, order_id: int) -> Order | None:
    """
    Obtiene un pedido por su ID, cargando sus items.

    Args:
        session: Sesión de SQLAlchemy
        order_id: ID del pedido

    Returns:
        Pedido encontrado o None si no existe
    """
    stmt = select(Order).where(Order.id == order_id).options(selectinload(Order.items))
    return session.scalars(stmt).first()


def get_orders_by_user(session: Session, user_id: int) -> list[Order]:
    """
    Obtiene todos los pedidos de un usuario.

    Args:
        session: Sesión de SQLAlchemy
        user_id: ID del usuario

    Returns:
        Lista de pedidos del usuario
    """
    stmt = (
        select(Order)
        .where(Order.user_id == user_id)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc())
    )
    return list(session.scalars(stmt).all())


def get_all_orders(session: Session, limit: int = 100) -> list[Order]:
    """
    Obtiene todos los pedidos del sistema.

    Args:
        session: Sesión de SQLAlchemy
        limit: Número máximo de pedidos a retornar

    Returns:
        Lista de pedidos
    """
    stmt = select(Order).options(selectinload(Order.items)).limit(limit)
    return list(session.scalars(stmt).all())


def update_order_status(session: Session, order_id: int, status: str) -> Order | None:
    """
    Actualiza el estado de un pedido.

    Args:
        session: Sesión de SQLAlchemy
        order_id: ID del pedido
        status: Nuevo estado ('pending', 'processing', 'completed', 'cancelled')

    Returns:
        Pedido actualizado o None si no existe
    """
    order = get_order_by_id(session, order_id)
    if not order:
        return None

    order.status = status
    session.commit()
    session.refresh(order)
    return order


def recalculate_order_total(session: Session, order_id: int) -> Order | None:
    """
    Recalcula el total de un pedido sumando sus items.

    Args:
        session: Sesión de SQLAlchemy
        order_id: ID del pedido

    Returns:
        Pedido actualizado o None si no existe
    """
    order = get_order_by_id(session, order_id)
    if not order:
        return None

    order.total = order.calculate_total()
    session.commit()
    session.refresh(order)
    return order


def delete_order(session: Session, order_id: int) -> bool:
    """
    Elimina un pedido y todos sus items (cascade).

    Args:
        session: Sesión de SQLAlchemy
        order_id: ID del pedido a eliminar

    Returns:
        True si se eliminó, False si no existía
    """
    order = get_order_by_id(session, order_id)
    if not order:
        return False

    session.delete(order)
    session.commit()
    return True


# ============================================================================
# CRUD para OrderItem
# ============================================================================


def add_item_to_order(
    session: Session,
    order_id: int,
    product_name: str,
    quantity: int,
    unit_price: Decimal,
) -> OrderItem | None:
    """
    Agrega un item a un pedido.

    Args:
        session: Sesión de SQLAlchemy
        order_id: ID del pedido
        product_name: Nombre del producto
        quantity: Cantidad de unidades
        unit_price: Precio unitario

    Returns:
        Item creado o None si el pedido no existe
    """
    order = get_order_by_id(session, order_id)
    if not order:
        return None

    subtotal = Decimal(str(quantity)) * unit_price

    item = OrderItem(
        order_id=order_id,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price,
        subtotal=subtotal,
    )
    session.add(item)
    session.commit()
    session.refresh(item)

    # Recalcular total del pedido
    recalculate_order_total(session, order_id)

    return item


def get_item_by_id(session: Session, item_id: int) -> OrderItem | None:
    """
    Obtiene un item por su ID.

    Args:
        session: Sesión de SQLAlchemy
        item_id: ID del item

    Returns:
        Item encontrado o None si no existe
    """
    return session.get(OrderItem, item_id)


def get_items_by_order(session: Session, order_id: int) -> list[OrderItem]:
    """
    Obtiene todos los items de un pedido.

    Args:
        session: Sesión de SQLAlchemy
        order_id: ID del pedido

    Returns:
        Lista de items del pedido
    """
    stmt = select(OrderItem).where(OrderItem.order_id == order_id)
    return list(session.scalars(stmt).all())


def update_item_quantity(
    session: Session, item_id: int, quantity: int
) -> OrderItem | None:
    """
    Actualiza la cantidad de un item y recalcula su subtotal.

    Args:
        session: Sesión de SQLAlchemy
        item_id: ID del item
        quantity: Nueva cantidad

    Returns:
        Item actualizado o None si no existe
    """
    item = get_item_by_id(session, item_id)
    if not item:
        return None

    item.quantity = quantity
    item.subtotal = item.calculate_subtotal()
    session.commit()
    session.refresh(item)

    # Recalcular total del pedido
    recalculate_order_total(session, item.order_id)

    return item


def delete_item(session: Session, item_id: int) -> bool:
    """
    Elimina un item de un pedido.

    Args:
        session: Sesión de SQLAlchemy
        item_id: ID del item a eliminar

    Returns:
        True si se eliminó, False si no existía
    """
    item = get_item_by_id(session, item_id)
    if not item:
        return False

    order_id = item.order_id
    session.delete(item)
    session.commit()

    # Recalcular total del pedido
    recalculate_order_total(session, order_id)

    return True
