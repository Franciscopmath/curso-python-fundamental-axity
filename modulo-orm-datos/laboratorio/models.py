"""
Modelos de SQLAlchemy para el sistema de pedidos.

Este módulo define las entidades User, Order y OrderItem con sus relaciones.
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Clase base para todos los modelos."""

    pass


class User(Base):
    """Modelo de usuario del sistema."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relación uno a muchos con Order
    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class Order(Base):
    """Modelo de pedido/orden de compra."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0.00)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'cancelled')",
            name="check_order_status",
        ),
        CheckConstraint("total >= 0", name="check_total_positive"),
    )

    # Relación muchos a uno con User
    user: Mapped["User"] = relationship("User", back_populates="orders")

    # Relación uno a muchos con OrderItem
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Order(id={self.id}, user_id={self.user_id}, "
            f"status='{self.status}', total={self.total})>"
        )

    def calculate_total(self) -> Decimal:
        """Calcula el total sumando todos los items."""
        return sum((item.subtotal for item in self.items), Decimal("0.00"))


class OrderItem(Base):
    """Modelo de item/producto dentro de un pedido."""

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id"), nullable=False
    )
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="check_unit_price_positive"),
        CheckConstraint("subtotal >= 0", name="check_subtotal_positive"),
    )

    # Relación muchos a uno con Order
    order: Mapped["Order"] = relationship("Order", back_populates="items")

    def __repr__(self) -> str:
        return (
            f"<OrderItem(id={self.id}, order_id={self.order_id}, "
            f"product='{self.product_name}', qty={self.quantity}, "
            f"subtotal={self.subtotal})>"
        )

    def calculate_subtotal(self) -> Decimal:
        """Calcula el subtotal multiplicando cantidad por precio unitario."""
        return Decimal(str(self.quantity)) * self.unit_price
