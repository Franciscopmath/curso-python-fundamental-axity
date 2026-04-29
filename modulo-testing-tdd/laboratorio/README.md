# Laboratorio: Testing y TDD

Sistema de inventario implementado con Test-Driven Development (TDD), mocking e Hypothesis.

## Estructura

```
laboratorio/
├── src/
│   ├── inventory.py              # Sistema de inventario (implementado con TDD)
│   └── notification_service.py   # Servicio para demostrar mocking
├── tests/
│   ├── conftest.py               # Fixtures compartidos
│   ├── test_inventory_tdd.py     # Tests TDD (escritos PRIMERO)
│   ├── test_mocking.py           # Tests con unittest.mock
│   └── test_hypothesis.py        # Property-based testing
├── pyproject.toml
└── README.md
```

## Instalación

```bash
poetry install
```

## Ciclo TDD Aplicado

### Red → Green → Refactor

**1. RED**: Escribir test que falla
```python
def test_create_product():
    product = Product("P001", "Laptop", Decimal("999.99"), 10)
    assert product.id == "P001"  # ❌ FALLA (Product no existe aún)
```

**2. GREEN**: Implementar código mínimo
```python
class Product:
    def __init__(self, id, name, price, stock):
        self.id = id  # ✅ PASA
```

**3. REFACTOR**: Mejorar código
```python
class Product:
    def __init__(self, id: str, name: str, price: Decimal, stock: int):
        if price <= 0:
            raise ValueError("Price must be positive")
        self.id = id
```

## Ejecutar Tests

### Todos los tests
```bash
poetry run pytest
```

### Con cobertura
```bash
poetry run pytest --cov=src --cov-report=html
```

### Por markers
```bash
# Solo tests unitarios
poetry run pytest -m unit

# Solo tests de integración
poetry run pytest -m integration

# Solo property-based tests
poetry run pytest -m property

# Excluir tests lentos
poetry run pytest -m "not slow"
```

### Tests específicos
```bash
# Solo TDD tests
poetry run pytest tests/test_inventory_tdd.py -v

# Solo mocking tests
poetry run pytest tests/test_mocking.py -v

# Solo Hypothesis tests
poetry run pytest tests/test_hypothesis.py -v
```

## Características Implementadas

### 1. TDD (test_inventory_tdd.py)
- ✅ 30+ tests escritos ANTES de la implementación
- ✅ Ciclo Red-Green-Refactor completo
- ✅ Tests parametrizados
- ✅ Fixtures de pytest
- ✅ Markers (unit, integration, slow)

### 2. Mocking (test_mocking.py)
- ✅ Mock de servicios externos (NotificationService)
- ✅ Verificación de llamadas (assert_called_once)
- ✅ Mock de respuestas (return_value, side_effect)
- ✅ Patch de clases y funciones
- ✅ Mock de excepciones

### 3. Property-Based Testing (test_hypothesis.py)
- ✅ Generación automática de casos con Hypothesis
- ✅ Tests de propiedades invariantes
- ✅ Strategies personalizados
- ✅ Examples explícitos para casos borde
- ✅ Assume para filtrar casos

### 4. Cobertura
- ✅ Configuración en pyproject.toml
- ✅ Reporte HTML y terminal
- ✅ Exclusión de líneas no testables
- ✅ Meta: >90% de cobertura

## Ejemplos de Uso

### Fixtures
```python
def test_with_fixture(inventory_with_products):
    assert len(inventory_with_products.products) == 3
```

### Parametrización
```python
@pytest.mark.parametrize("stock,decrease,expected", [
    (100, 10, 90),
    (50, 25, 25),
])
def test_scenarios(stock, decrease, expected):
    ...
```

### Mocking
```python
def test_notification(mocker):
    mock_service = mocker.Mock()
    notifier = InventoryNotifier(mock_service)
    notifier.notify_low_stock("P001", "Mouse", 2)
    mock_service.send_notification.assert_called_once()
```

### Property-Based
```python
@given(stock=st.integers(min_value=0, max_value=1000))
def test_stock_never_negative(stock):
    product = Product("P001", "Test", Decimal("10"), stock)
    assert product.stock >= 0
```

## Métricas de Cobertura

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

Resultado esperado:
```
src/inventory.py              100%
src/notification_service.py   95%
-----------------------------------
TOTAL                          98%
```

## Mejores Prácticas Aplicadas

1. **TDD Estricto**: Tests escritos ANTES del código
2. **Tests Aislados**: Cada test independiente
3. **Fixtures Reutilizables**: conftest.py centralizado
4. **Nombres Descriptivos**: test_*_does_what
5. **Arrange-Act-Assert**: Estructura clara
6. **Cobertura Alta**: >90% de líneas
7. **Fast Tests**: Mayoría < 1ms
8. **Markers**: Organización por tipo

## CI/CD Integration

El `pyproject.toml` está configurado para CI:

```bash
# En GitHub Actions / GitLab CI
poetry install
poetry run pytest --cov=src --cov-report=xml
# Upload coverage to Codecov
```

## Objetivos Cumplidos

✅ Implementar funcionalidad con TDD
✅ Fixtures y parametrización de pytest
✅ Mocking con unittest.mock
✅ Property-based testing con Hypothesis
✅ Cobertura >90%
✅ Markers para organizar tests
✅ Reporte de cobertura HTML
✅ Suite estable y confiable
