"""
Modelo de Pedido para SQLAlchemy.
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Order(Base):
    """Modelo de pedido/orden de compra."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Constraints
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="check_unit_price_positive"),
        CheckConstraint("total >= 0", name="check_total_positive"),
        CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'cancelled')",
            name="check_order_status",
        ),
    )

    # Relación con usuario
    user: Mapped["User"] = relationship("User", back_populates="orders")

    def __repr__(self) -> str:
        return (
            f"<Order(id={self.id}, user_id={self.user_id}, "
            f"product='{self.product_name}', total={self.total})>"
        )

    def calculate_total(self) -> Decimal:
        """Calcula el total del pedido."""
        return Decimal(str(self.quantity)) * self.unit_price
