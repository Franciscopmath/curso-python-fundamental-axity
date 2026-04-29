"""
Configuración de pytest y fixtures compartidos.
"""

import pytest
from decimal import Decimal
from src.inventory import Inventory, Product


@pytest.fixture
def empty_inventory():
    """Fixture: Inventario vacío."""
    return Inventory()


@pytest.fixture
def sample_product():
    """Fixture: Producto de ejemplo."""
    return Product("P001", "Sample Product", Decimal("99.99"), 10)


@pytest.fixture
def inventory_with_products():
    """Fixture: Inventario con varios productos."""
    inventory = Inventory()
    inventory.add_product(Product("P001", "Laptop", Decimal("1299.99"), 5))
    inventory.add_product(Product("P002", "Mouse", Decimal("25.50"), 50))
    inventory.add_product(Product("P003", "Keyboard", Decimal("75.00"), 20))
    return inventory


@pytest.fixture
def low_stock_products():
    """Fixture: Productos con stock bajo."""
    inventory = Inventory()
    inventory.add_product(Product("P001", "Monitor", Decimal("299.99"), 2))
    inventory.add_product(Product("P002", "Webcam", Decimal("89.99"), 1))
    return inventory
