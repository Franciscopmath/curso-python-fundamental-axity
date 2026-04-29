"""
Property-based testing con Hypothesis.

Hypothesis genera automáticamente casos de prueba para verificar propiedades.
"""

import pytest
from decimal import Decimal
from hypothesis import given, strategies as st, assume, example
from src.inventory import Product, Inventory, InvalidProductError


# ============================================================================
# Property-based tests para Product
# ============================================================================


@pytest.mark.property
class TestProductProperties:
    """Tests de propiedades de Product."""

    @given(
        product_id=st.text(min_size=1, max_size=50),
        name=st.text(min_size=1, max_size=100),
        price=st.decimals(
            min_value="0.01", max_value="999999.99", places=2, allow_nan=False
        ),
        stock=st.integers(min_value=0, max_value=100000),
    )
    def test_product_creation_with_valid_data(
        self, product_id, name, price, stock
    ):
        """Propiedad: Cualquier producto con datos válidos se crea correctamente."""
        product = Product(product_id, name, price, stock)

        assert product.id == product_id
        assert product.name == name
        assert product.price == price
        assert product.stock == stock

    @given(
        price=st.decimals(
            min_value="-999999.99", max_value="0.00", places=2, allow_nan=False
        )
    )
    @example(price=Decimal("0.00"))  # Caso borde explícito
    @example(price=Decimal("-0.01"))
    def test_product_price_must_be_positive_property(self, price):
        """Propiedad: Precios no positivos deben lanzar ValueError."""
        with pytest.raises(ValueError):
            Product("P001", "Test", price, 10)

    @given(stock=st.integers(max_value=-1))
    @example(stock=-1)  # Caso borde
    @example(stock=-100)
    def test_product_stock_cannot_be_negative_property(self, stock):
        """Propiedad: Stock negativo debe lanzar ValueError."""
        with pytest.raises(ValueError):
            Product("P001", "Test", Decimal("10"), stock)


# ============================================================================
# Property-based tests para Inventory
# ============================================================================


@pytest.mark.property
class TestInventoryProperties:
    """Tests de propiedades de Inventory."""

    @given(
        products=st.lists(
            st.tuples(
                st.text(min_size=1, max_size=20),  # id
                st.text(min_size=1, max_size=50),  # name
                st.decimals(min_value="0.01", max_value="1000", places=2),  # price
                st.integers(min_value=0, max_value=100),  # stock
            ),
            min_size=0,
            max_size=50,
            unique_by=lambda x: x[0],  # IDs únicos
        )
    )
    def test_inventory_size_matches_added_products(self, products):
        """Propiedad: El tamaño del inventario coincide con productos agregados."""
        inventory = Inventory()

        for product_id, name, price, stock in products:
            inventory.add_product(Product(product_id, name, price, stock))

        assert len(inventory.products) == len(products)

    @given(
        initial_stock=st.integers(min_value=0, max_value=1000),
        increase_amount=st.integers(min_value=1, max_value=500),
    )
    def test_increase_stock_property(self, initial_stock, increase_amount):
        """Propiedad: Incrementar stock siempre aumenta la cantidad."""
        inventory = Inventory()
        product = Product("P001", "Test", Decimal("10"), initial_stock)
        inventory.add_product(product)

        inventory.increase_stock("P001", increase_amount)

        assert inventory.get_product("P001").stock == initial_stock + increase_amount

    @given(
        initial_stock=st.integers(min_value=10, max_value=1000),
        decrease_amount=st.integers(min_value=1, max_value=9),
    )
    def test_decrease_stock_property(self, initial_stock, decrease_amount):
        """Propiedad: Decrementar stock válido siempre reduce la cantidad."""
        # Asegurar que decrease_amount <= initial_stock
        assume(decrease_amount <= initial_stock)

        inventory = Inventory()
        product = Product("P001", "Test", Decimal("10"), initial_stock)
        inventory.add_product(product)

        inventory.decrease_stock("P001", decrease_amount)

        assert inventory.get_product("P001").stock == initial_stock - decrease_amount

    @given(
        products=st.lists(
            st.tuples(
                st.text(min_size=1, max_size=10, alphabet=st.characters(blacklist_characters="\x00")),
                st.text(min_size=1, max_size=30),
                st.decimals(min_value="1", max_value="100", places=2),
                st.integers(min_value=1, max_value=10),
            ),
            min_size=1,
            max_size=20,
            unique_by=lambda x: x[0],
        )
    )
    def test_total_value_property(self, products):
        """Propiedad: Valor total es la suma de (precio * stock)."""
        inventory = Inventory()
        expected_total = Decimal("0")

        for product_id, name, price, stock in products:
            inventory.add_product(Product(product_id, name, price, stock))
            expected_total += price * stock

        assert inventory.total_value() == expected_total

    @given(
        product_id=st.text(min_size=1, max_size=20),
        quantity_available=st.integers(min_value=0, max_value=100),
        quantity_requested=st.integers(min_value=0, max_value=150),
    )
    def test_availability_check_property(
        self, product_id, quantity_available, quantity_requested
    ):
        """Propiedad: is_available retorna True ssi stock >= cantidad."""
        inventory = Inventory()
        product = Product(product_id, "Test", Decimal("10"), quantity_available)
        inventory.add_product(product)

        result = inventory.is_available(product_id, quantity_requested)

        assert result == (quantity_available >= quantity_requested)


# ============================================================================
# Property-based tests con invariantes
# ============================================================================


@pytest.mark.property
class TestInventoryInvariants:
    """Tests de invariantes del sistema."""

    @given(
        operations=st.lists(
            st.one_of(
                st.tuples(st.just("increase"), st.integers(min_value=1, max_value=50)),
                st.tuples(st.just("decrease"), st.integers(min_value=1, max_value=10)),
            ),
            min_size=1,
            max_size=20,
        )
    )
    def test_stock_never_negative_invariant(self, operations):
        """Invariante: El stock nunca debe ser negativo."""
        inventory = Inventory()
        initial_stock = 1000  # Stock inicial alto
        product = Product("P001", "Test", Decimal("10"), initial_stock)
        inventory.add_product(product)

        current_stock = initial_stock

        for operation, amount in operations:
            try:
                if operation == "increase":
                    inventory.increase_stock("P001", amount)
                    current_stock += amount
                elif operation == "decrease":
                    if current_stock >= amount:  # Solo si hay suficiente
                        inventory.decrease_stock("P001", amount)
                        current_stock -= amount
            except Exception:
                pass  # Ignorar errores esperados

        # Invariante: stock nunca negativo
        assert inventory.get_product("P001").stock >= 0
