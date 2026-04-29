"""
Sistema de inventario de productos.

Implementado siguiendo TDD (Test-Driven Development).
Los tests se escribieron primero en test_inventory_tdd.py
"""

from decimal import Decimal


class InvalidProductError(Exception):
    """Excepción para operaciones inválidas con productos."""

    pass


class InsufficientStockError(Exception):
    """Excepción para stock insuficiente."""

    pass


class Product:
    """
    Representa un producto en el inventario.

    Attributes:
        id: Identificador único del producto
        name: Nombre del producto
        price: Precio unitario (Decimal para precisión)
        stock: Cantidad disponible en inventario
    """

    def __init__(self, id: str, name: str, price: Decimal, stock: int):
        """
        Crea un nuevo producto.

        Args:
            id: Identificador único
            name: Nombre del producto
            price: Precio unitario (debe ser positivo)
            stock: Cantidad inicial (no puede ser negativo)

        Raises:
            ValueError: Si price <= 0 o stock < 0
        """
        if price <= 0:
            raise ValueError("Price must be positive")
        if stock < 0:
            raise ValueError("Stock cannot be negative")

        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self) -> str:
        return (
            f"Product(id='{self.id}', name='{self.name}', "
            f"price={self.price}, stock={self.stock})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return False
        return self.id == other.id


class Inventory:
    """
    Gestiona un inventario de productos.

    Permite agregar, eliminar, y gestionar stock de productos.
    """

    def __init__(self):
        """Crea un inventario vacío."""
        self.products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        """
        Agrega un producto al inventario.

        Args:
            product: Producto a agregar

        Raises:
            InvalidProductError: Si el producto ya existe
        """
        if product.id in self.products:
            raise InvalidProductError(
                f"Product with ID '{product.id}' already exists"
            )
        self.products[product.id] = product

    def get_product(self, product_id: str) -> Product | None:
        """
        Obtiene un producto por su ID.

        Args:
            product_id: ID del producto

        Returns:
            Producto si existe, None en caso contrario
        """
        return self.products.get(product_id)

    def remove_product(self, product_id: str) -> None:
        """
        Elimina un producto del inventario.

        Args:
            product_id: ID del producto a eliminar

        Raises:
            InvalidProductError: Si el producto no existe
        """
        if product_id not in self.products:
            raise InvalidProductError(f"Product '{product_id}' not found")
        del self.products[product_id]

    def increase_stock(self, product_id: str, quantity: int) -> None:
        """
        Incrementa el stock de un producto.

        Args:
            product_id: ID del producto
            quantity: Cantidad a incrementar

        Raises:
            ValueError: Si quantity <= 0
            InvalidProductError: Si el producto no existe
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        product = self.get_product(product_id)
        if not product:
            raise InvalidProductError(f"Product '{product_id}' not found")

        product.stock += quantity

    def decrease_stock(self, product_id: str, quantity: int) -> None:
        """
        Decrementa el stock de un producto.

        Args:
            product_id: ID del producto
            quantity: Cantidad a decrementar

        Raises:
            ValueError: Si quantity <= 0
            InvalidProductError: Si el producto no existe
            InsufficientStockError: Si no hay stock suficiente
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        product = self.get_product(product_id)
        if not product:
            raise InvalidProductError(f"Product '{product_id}' not found")

        if product.stock < quantity:
            raise InsufficientStockError(
                f"Insufficient stock for '{product_id}'. "
                f"Available: {product.stock}, Requested: {quantity}"
            )

        product.stock -= quantity

    def is_available(self, product_id: str, quantity: int) -> bool:
        """
        Verifica si hay stock suficiente de un producto.

        Args:
            product_id: ID del producto
            quantity: Cantidad requerida

        Returns:
            True si hay stock suficiente, False en caso contrario
        """
        product = self.get_product(product_id)
        if not product:
            return False
        return product.stock >= quantity

    def total_value(self) -> Decimal:
        """
        Calcula el valor total del inventario.

        Returns:
            Suma de (precio * stock) de todos los productos
        """
        return sum(
            (product.price * product.stock for product in self.products.values()),
            Decimal("0"),
        )
