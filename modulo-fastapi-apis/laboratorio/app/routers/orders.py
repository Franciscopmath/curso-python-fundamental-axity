"""
Router de pedidos (Orders).

Maneja CRUD completo de pedidos con autenticación requerida.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo pedido para el usuario autenticado.

    Args:
        order_data: Datos del pedido (product_name, quantity, unit_price)
        current_user: Usuario autenticado
        db: Sesión de base de datos

    Returns:
        Pedido creado con total calculado
    """
    # Calcular total
    total = order_data.quantity * order_data.unit_price

    # Crear pedido
    db_order = Order(
        user_id=current_user.id,
        product_name=order_data.product_name,
        quantity=order_data.quantity,
        unit_price=order_data.unit_price,
        total=total,
        status="pending",
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


@router.get("/", response_model=list[OrderResponse], summary="List all orders")
def list_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Lista todos los pedidos del usuario autenticado.

    Args:
        skip: Número de registros a omitir (paginación)
        limit: Número máximo de registros a retornar
        current_user: Usuario autenticado
        db: Sesión de base de datos

    Returns:
        Lista de pedidos del usuario
    """
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return orders


@router.get("/{order_id}", response_model=OrderResponse, summary="Get order by ID")
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Obtiene un pedido específico por su ID.

    Args:
        order_id: ID del pedido
        current_user: Usuario autenticado
        db: Sesión de base de datos

    Returns:
        Pedido solicitado

    Raises:
        HTTPException 404: Si el pedido no existe
        HTTPException 403: Si el pedido no pertenece al usuario
    """
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Verificar que el pedido pertenezca al usuario autenticado
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order",
        )

    return order


@router.put("/{order_id}", response_model=OrderResponse, summary="Update order")
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Actualiza un pedido existente.

    Args:
        order_id: ID del pedido
        order_update: Datos a actualizar (product_name, quantity, unit_price, status)
        current_user: Usuario autenticado
        db: Sesión de base de datos

    Returns:
        Pedido actualizado

    Raises:
        HTTPException 404: Si el pedido no existe
        HTTPException 403: Si el pedido no pertenece al usuario
    """
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Verificar que el pedido pertenezca al usuario autenticado
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this order",
        )

    # Actualizar campos si se proporcionan
    update_data = order_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(order, field, value)

    # Recalcular total si cambió quantity o unit_price
    if "quantity" in update_data or "unit_price" in update_data:
        order.total = order.calculate_total()

    db.commit()
    db.refresh(order)

    return order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete order",
)
def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Elimina un pedido.

    Args:
        order_id: ID del pedido
        current_user: Usuario autenticado
        db: Sesión de base de datos

    Raises:
        HTTPException 404: Si el pedido no existe
        HTTPException 403: Si el pedido no pertenece al usuario
    """
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Verificar que el pedido pertenezca al usuario autenticado
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this order",
        )

    db.delete(order)
    db.commit()
