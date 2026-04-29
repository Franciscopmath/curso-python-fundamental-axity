"""
Schemas Pydantic para pedidos (Orders).
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class OrderBase(BaseModel):
    """Base schema para Order."""

    product_name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., gt=0, le=10000)
    unit_price: Decimal = Field(..., gt=0, decimal_places=2)


class OrderCreate(OrderBase):
    """Schema para crear un pedido."""

    @field_validator("product_name")
    @classmethod
    def validate_product_name(cls, v: str) -> str:
        """Valida que no haya espacios al inicio/final."""
        if v.strip() != v:
            raise ValueError("Product name cannot have leading/trailing whitespace")
        return v


class OrderUpdate(BaseModel):
    """Schema para actualizar un pedido."""

    product_name: str | None = Field(None, min_length=1, max_length=200)
    quantity: int | None = Field(None, gt=0, le=10000)
    unit_price: Decimal | None = Field(None, gt=0, decimal_places=2)
    status: str | None = Field(None, pattern="^(pending|processing|completed|cancelled)$")

    @field_validator("product_name")
    @classmethod
    def validate_product_name(cls, v: str | None) -> str | None:
        """Valida que no haya espacios al inicio/final."""
        if v is not None and v.strip() != v:
            raise ValueError("Product name cannot have leading/trailing whitespace")
        return v


class OrderResponse(OrderBase):
    """Schema para respuesta de pedido."""

    id: int
    user_id: int
    total: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
