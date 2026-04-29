# Módulo 10: Pruebas y TDD

## Introducción

El testing es fundamental para garantizar la calidad del software. TDD (Test-Driven Development) invierte el proceso tradicional: escribimos tests ANTES del código de producción.

**Ciclo TDD: Red → Green → Refactor**

1. **Red**: Escribir un test que falla
2. **Green**: Escribir el código mínimo para que pase
3. **Refactor**: Mejorar el código sin romper tests

---

## 1. pytest: Framework de Testing Moderno

### Instalación
```bash
pip install pytest pytest-cov pytest-mock
```

### Tests Básicos
```python
def test_addition():
    assert 2 + 2 == 4

def test_string_length():
    assert len("hello") == 5
```

### Fixtures
Reutilizan setup común:

```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "John", "age": 30}

def test_with_fixture(sample_data):
    assert sample_data["name"] == "John"
```

### Parametrización
Múltiples casos en un test:

```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

### Markers
Organizan y filtran tests:

```python
@pytest.mark.slow
def test_large_computation():
    ...

@pytest.mark.integration
def test_database():
    ...

# Ejecutar: pytest -m "not slow"
```

---

## 2. Mocking con unittest.mock

Mock simula dependencias externas (APIs, BD, servicios).

### Mock Básico
```python
from unittest.mock import Mock

service = Mock()
service.get_data.return_value = {"status": "ok"}

result = service.get_data()
assert result["status"] == "ok"
service.get_data.assert_called_once()
```

### Patch
Reemplaza temporalmente objetos:

```python
from unittest.mock import patch

@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"data": [1, 2, 3]}

    import requests
    response = requests.get("https://api.example.com")

    assert response.json()["data"] == [1, 2, 3]
```

### pytest-mock
Plugin más pythonic:

```python
def test_with_mocker(mocker):
    mock_service = mocker.Mock()
    mock_service.process.return_value = True

    assert mock_service.process() is True
```

---

## 3. Property-Based Testing con Hypothesis

Hypothesis genera automáticamente casos de prueba.

### Instalación
```bash
pip install hypothesis
```

### Test Basado en Propiedades
```python
from hypothesis import given, strategies as st

@given(x=st.integers(), y=st.integers())
def test_commutative_addition(x, y):
    assert x + y == y + x  # Propiedad: suma es conmutativa
```

### Strategies Comunes
```python
st.integers(min_value=0, max_value=100)
st.text(min_size=1, max_size=50)
st.lists(st.integers(), min_size=0, max_size=10)
st.decimals(min_value="0.01", max_value="999.99", places=2)
```

### Examples Explícitos
```python
from hypothesis import example

@given(x=st.integers())
@example(x=0)  # Caso borde explícito
@example(x=-1)
def test_abs_positive(x):
    assert abs(x) >= 0
```

---

## 4. Cobertura de Código

### pytest-cov
```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
```

### Configuración en pyproject.toml
```toml
[tool.coverage.run]
source = ["src"]
omit = ["tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
]
```

### Meta de Cobertura
- **80-90%**: Buena cobertura
- **>90%**: Excelente cobertura
- **100%**: No siempre necesario ni práctico

---

## 5. Integración en CI/CD

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install poetry
      - run: poetry install
      - run: poetry run pytest --cov=src
      - uses: codecov/codecov-action@v2
```

### GitLab CI
```yaml
test:
  script:
    - poetry install
    - poetry run pytest --cov=src --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
```

---

## 6. TDD en Práctica

### Ejemplo Completo

**1. Test (Red)**
```python
def test_bank_account_deposit():
    account = BankAccount(balance=100)
    account.deposit(50)
    assert account.balance == 150  # ❌ FALLA
```

**2. Implementación (Green)**
```python
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount  # ✅ PASA
```

**3. Refactor**
```python
class BankAccount:
    def __init__(self, balance: Decimal = Decimal("0")):
        if balance < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = balance

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    @property
    def balance(self) -> Decimal:
        return self._balance
```

---

## 7. Mejores Prácticas

1. **Tests Aislados**: Cada test independiente
2. **Nombres Descriptivos**: `test_user_cannot_withdraw_more_than_balance`
3. **Arrange-Act-Assert**: Estructura clara
4. **Un Assert por Test**: Facilita debug
5. **Fast Tests**: Suite completa < 10s
6. **No Lógica en Tests**: Tests simples y directos
7. **Test Código Crítico**: Priorizar funcionalidad importante

---

## 8. Recursos

- [pytest Documentation](https://docs.pytest.org/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Test-Driven Development by Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530) - Kent Beck
- [Python Testing with pytest](https://pragprog.com/titles/bopytest/) - Brian Okken

---

## Conclusión

TDD y testing automatizado son esenciales para:
- ✅ Detectar bugs temprano
- ✅ Facilitar refactoring
- ✅ Documentar comportamiento
- ✅ Mejorar diseño de código
- ✅ Dar confianza para cambios

El laboratorio demuestra TDD real con pytest, mocking e Hypothesis.
