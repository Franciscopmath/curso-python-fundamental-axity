"""
Tests TDD para sistema de inventario.

Este archivo sigue el ciclo Red-Green-Refactor de TDD.
Los tests se escribieron ANTES que la implementación.
"""

import pytest
from decimal import Decimal
from src.inventory import Inventory, Product, InsufficientStockError, InvalidProductError


# ============================================================================
# Tests Básicos - Ciclo TDD 1: Crear Producto
# ============================================================================


class TestProductCreation:
    """Tests para creación de productos."""

    def test_create_product_with_valid_data(self):
        """Test: Crear producto con datos válidos."""
        product = Product(
            id="PROD001",
            name="Laptop",
            price=Decimal("999.99"),
            stock=10
        )
        assert product.id == "PROD001"
        assert product.name == "Laptop"
        assert product.price == Decimal("999.99")
        assert product.stock == 10

    def test_product_price_must_be_positive(self):
        """Test: El precio debe ser positivo."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Product(id="P001", name="Item", price=Decimal("-10"), stock=5)

    def test_product_stock_must_be_non_negative(self):
        """Test: El stock no puede ser negativo."""
        with pytest.raises(ValueError, match="Stock cannot be negative"):
            Product(id="P001", name="Item", price=Decimal("10"), stock=-1)


# ============================================================================
# Tests de Inventario - Ciclo TDD 2: Gestión de Inventario
# ============================================================================


class TestInventoryBasics:
    """Tests básicos del inventario."""

    @pytest.fixture
    def inventory(self):
        """Fixture: inventario vacío."""
        return Inventory()

    @pytest.fixture
    def sample_product(self):
        """Fixture: producto de ejemplo."""
        return Product("P001", "Mouse", Decimal("25.99"), 50)

    def test_create_empty_inventory(self, inventory):
        """Test: Crear inventario vacío."""
        assert len(inventory.products) == 0

    def test_add_product_to_inventory(self, inventory, sample_product):
        """Test: Agregar producto al inventario."""
        inventory.add_product(sample_product)
        assert len(inventory.products) == 1
        assert inventory.get_product("P001") == sample_product

    def test_add_duplicate_product_raises_error(self, inventory, sample_product):
        """Test: Agregar producto duplicado lanza error."""
        inventory.add_product(sample_product)
        with pytest.raises(InvalidProductError, match="already exists"):
            inventory.add_product(sample_product)

    def test_get_nonexistent_product_returns_none(self, inventory):
        """Test: Obtener producto inexistente retorna None."""
        assert inventory.get_product("NONEXISTENT") is None

    def test_remove_product_from_inventory(self, inventory, sample_product):
        """Test: Eliminar producto del inventario."""
        inventory.add_product(sample_product)
        inventory.remove_product("P001")
        assert len(inventory.products) == 0

    def test_remove_nonexistent_product_raises_error(self, inventory):
        """Test: Eliminar producto inexistente lanza error."""
        with pytest.raises(InvalidProductError, match="not found"):
            inventory.remove_product("NONEXISTENT")


# ============================================================================
# Tests de Stock - Ciclo TDD 3: Gestión de Stock
# ============================================================================


class TestStockManagement:
    """Tests para gestión de stock."""

    @pytest.fixture
    def inventory_with_products(self):
        """Fixture: inventario con productos."""
        inv = Inventory()
        inv.add_product(Product("P001", "Keyboard", Decimal("75.00"), 20))
        inv.add_product(Product("P002", "Monitor", Decimal("299.99"), 5))
        return inv

    def test_increase_stock(self, inventory_with_products):
        """Test: Incrementar stock de producto."""
        inventory_with_products.increase_stock("P001", 10)
        product = inventory_with_products.get_product("P001")
        assert product.stock == 30

    def test_increase_stock_with_negative_raises_error(self, inventory_with_products):
        """Test: Incrementar con cantidad negativa lanza error."""
        with pytest.raises(ValueError, match="must be positive"):
            inventory_with_products.increase_stock("P001", -5)

    def test_decrease_stock(self, inventory_with_products):
        """Test: Decrementar stock de producto."""
        inventory_with_products.decrease_stock("P001", 5)
        product = inventory_with_products.get_product("P001")
        assert product.stock == 15

    def test_decrease_stock_insufficient_raises_error(self, inventory_with_products):
        """Test: Decrementar más del stock disponible lanza error."""
        with pytest.raises(InsufficientStockError):
            inventory_with_products.decrease_stock("P001", 100)

    def test_check_stock_availability_true(self, inventory_with_products):
        """Test: Verificar disponibilidad de stock (suficiente)."""
        assert inventory_with_products.is_available("P001", 10) is True

    def test_check_stock_availability_false(self, inventory_with_products):
        """Test: Verificar disponibilidad de stock (insuficiente)."""
        assert inventory_with_products.is_available("P001", 100) is False


# ============================================================================
# Tests Parametrizados - Ciclo TDD 4: Casos Múltiples
# ============================================================================


class TestInventoryWithParametrization:
    """Tests parametrizados para múltiples escenarios."""

    @pytest.mark.parametrize(
        "product_id,name,price,stock",
        [
            ("P001", "Item1", Decimal("10.00"), 5),
            ("P002", "Item2", Decimal("25.50"), 10),
            ("P003", "Item3", Decimal("100.99"), 1),
        ],
    )
    def test_add_multiple_products(self, product_id, name, price, stock):
        """Test parametrizado: agregar varios productos."""
        inventory = Inventory()
        product = Product(product_id, name, price, stock)
        inventory.add_product(product)
        assert inventory.get_product(product_id).name == name

    @pytest.mark.parametrize(
        "initial_stock,decrease_amount,expected_stock",
        [
            (100, 10, 90),
            (50, 25, 25),
            (10, 10, 0),
        ],
    )
    def test_stock_decrease_scenarios(
        self, initial_stock, decrease_amount, expected_stock
    ):
        """Test parametrizado: escenarios de decremento de stock."""
        inventory = Inventory()
        product = Product("P001", "Item", Decimal("10"), initial_stock)
        inventory.add_product(product)
        inventory.decrease_stock("P001", decrease_amount)
        assert inventory.get_product("P001").stock == expected_stock


# ============================================================================
# Tests de Integración - Ciclo TDD 5: Flujos Completos
# ============================================================================


@pytest.mark.integration
class TestInventoryIntegration:
    """Tests de integración para flujos completos."""

    def test_complete_inventory_workflow(self):
        """Test: Flujo completo de gestión de inventario."""
        # 1. Crear inventario
        inventory = Inventory()

        # 2. Agregar productos
        inventory.add_product(Product("P001", "Laptop", Decimal("1200.00"), 10))
        inventory.add_product(Product("P002", "Mouse", Decimal("25.00"), 50))

        # 3. Verificar stock
        assert inventory.is_available("P001", 5) is True

        # 4. Vender (decrementar stock)
        inventory.decrease_stock("P001", 3)
        assert inventory.get_product("P001").stock == 7

        # 5. Reabastecer
        inventory.increase_stock("P001", 10)
        assert inventory.get_product("P001").stock == 17

        # 6. Eliminar producto agotado
        inventory.decrease_stock("P002", 50)
        inventory.remove_product("P002")
        assert len(inventory.products) == 1

    def test_total_inventory_value(self):
        """Test: Calcular valor total del inventario."""
        inventory = Inventory()
        inventory.add_product(Product("P001", "Item1", Decimal("10.00"), 5))
        inventory.add_product(Product("P002", "Item2", Decimal("25.00"), 2))

        # Total = (10 * 5) + (25 * 2) = 50 + 50 = 100
        assert inventory.total_value() == Decimal("100.00")


# ============================================================================
# Markers para organizar tests
# ============================================================================


@pytest.mark.unit
def test_product_repr():
    """Test: Representación string de producto."""
    product = Product("P001", "Test", Decimal("10"), 5)
    assert "P001" in repr(product)
    assert "Test" in repr(product)


@pytest.mark.slow
def test_large_inventory_performance():
    """Test marcado como slow: inventario grande."""
    inventory = Inventory()
    # Agregar 1000 productos
    for i in range(1000):
        inventory.add_product(
            Product(f"P{i:04d}", f"Product {i}", Decimal("10.00"), 10)
        )
    assert len(inventory.products) == 1000
