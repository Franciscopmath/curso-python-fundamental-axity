# Laboratorio: Tipado Estático Opcional y Calidad de Código

Sistema de gestión de biblioteca con type hints completos y verificación estática de tipos.

## Objetivos

Este laboratorio implementa:

1. **Type hints completos**: Anotaciones de tipos en todas las funciones y métodos
2. **Typing avanzado**: Union, Literal, TypedDict, Protocol, Generic types
3. **Verificación con mypy**: Análisis estático de tipos
4. **Cumplimiento de PEP 8**: Código conforme al estándar de Python
5. **Herramientas de calidad**: ruff, black, isort configurados
6. **Pre-commit hooks**: Verificaciones automáticas antes de commits
7. **Configuración para CI**: Listo para integración continua

## Estructura del Código

```
biblioteca_tipada.py
├── Constantes y Tipos
│   ├── Constantes con Final
│   ├── Type aliases (ISBN, UserID, BookID)
│   └── Literal types (TipoUsuario, EstadoLibro, CategoriaLibro)
├── Enumeraciones
│   └── EstadoPrestamo
├── TypedDict
│   ├── LibroDict
│   ├── UsuarioDict
│   └── PrestamoDict
├── Protocols
│   ├── Prestable
│   ├── Identificable
│   ├── Validable
│   └── Repositorio (genérico)
├── Generic Types
│   └── TypeVars y clases genéricas
├── Clases de Dominio
│   ├── Libro
│   ├── Usuario
│   └── Prestamo
├── Funciones con Types Avanzados
│   ├── Overloaded functions
│   ├── Funciones con Callable
│   ├── Funciones con generics
│   └── Generadores tipados
├── Sistema Principal
│   └── Clase Biblioteca
└── Ejemplos de Uso
    ├── ejemplo_basico()
    ├── ejemplo_type_hints_avanzados()
    └── ejemplo_validacion_tipos()
```

## Instalación

### 1. Instalar dependencias

```bash
cd modulo-tipado-calidad/laboratorio
poetry install
```

Esto instalará:
- **mypy**: Verificador de tipos estático
- **ruff**: Linter y formateador ultra rápido
- **black**: Formateador de código opinionado
- **isort**: Ordenador de imports
- **pre-commit**: Framework de hooks de Git
- **types-requests**: Stubs de tipos para requests

### 2. Activar el entorno virtual

```bash
poetry shell
```

### 3. Instalar pre-commit hooks

```bash
pre-commit install
```

## Uso

### Ejecutar el programa

```bash
python biblioteca_tipada.py
```

Esto ejecutará 3 ejemplos que demuestran:
1. Uso básico del sistema de biblioteca
2. Type hints avanzados en acción
3. Validación de tipos y errores

### Verificar tipos con mypy

```bash
# Verificación básica
poetry run mypy biblioteca_tipada.py

# Modo estricto (recomendado)
poetry run mypy --strict biblioteca_tipada.py

# Ver solo errores
poetry run mypy --no-error-summary biblioteca_tipada.py

# Generar reporte HTML
poetry run mypy --html-report mypy-report biblioteca_tipada.py
```

**Salida esperada:**
```
Success: no issues found in 1 source file
```

### Verificar calidad con ruff

```bash
# Verificar código
poetry run ruff check biblioteca_tipada.py

# Auto-corregir problemas
poetry run ruff check --fix biblioteca_tipada.py

# Formatear código
poetry run ruff format biblioteca_tipada.py

# Verificar todo
poetry run ruff check . && poetry run ruff format --check .
```

### Formatear con black

```bash
# Formatear código
poetry run black biblioteca_tipada.py

# Solo verificar (no modificar)
poetry run black --check biblioteca_tipada.py

# Ver diferencias
poetry run black --diff biblioteca_tipada.py
```

### Ordenar imports con isort

```bash
# Ordenar imports
poetry run isort biblioteca_tipada.py

# Solo verificar
poetry run isort --check biblioteca_tipada.py

# Ver diferencias
poetry run isort --diff biblioteca_tipada.py
```

### Ejecutar todas las herramientas

```bash
# Verificación completa
poetry run ruff check . && \
poetry run ruff format --check . && \
poetry run mypy biblioteca_tipada.py

# Auto-corregir y formatear
poetry run ruff check --fix . && \
poetry run ruff format . && \
poetry run isort .
```

## Pre-commit Hooks

Los hooks se ejecutan automáticamente al hacer commit:

```bash
git add biblioteca_tipada.py
git commit -m "feat: add biblioteca system"
```

**Hooks configurados:**
1. `trailing-whitespace`: Elimina espacios al final de líneas
2. `end-of-file-fixer`: Asegura nueva línea al final de archivos
3. `check-yaml`: Valida sintaxis YAML
4. `check-toml`: Valida sintaxis TOML
5. `check-added-large-files`: Previene commits de archivos grandes
6. `ruff`: Linter y formateador
7. `mypy`: Verificador de tipos

**Ejecutar hooks manualmente:**
```bash
# Todos los archivos
pre-commit run --all-files

# Solo un hook específico
pre-commit run mypy --all-files
pre-commit run ruff --all-files
```

## Conceptos Demostrados

### 1. Type Hints Básicos

```python
def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"

edad: int = 30
precio: float = 19.99
activo: bool = True
```

### 2. Colecciones Tipadas

```python
libros: list[Libro] = []
usuarios_por_id: dict[int, Usuario] = {}
categorias: set[str] = {"ficcion", "no_ficcion"}
coordenadas: tuple[float, float] = (10.5, 20.3)
```

### 3. Union Types

```python
# Python 3.10+
def procesar(valor: int | str) -> str:
    if isinstance(valor, int):
        return f"Número: {valor}"
    return f"Texto: {valor}"

# Opcional (equivalente a T | None)
def buscar_usuario(id: int) -> Usuario | None:
    ...
```

### 4. Literal Types

```python
from typing import Literal

TipoUsuario = Literal["estudiante", "profesor", "externo"]

def crear_usuario(tipo: TipoUsuario) -> Usuario:
    # Solo acepta "estudiante", "profesor", o "externo"
    ...
```

### 5. TypedDict

```python
from typing import TypedDict

class LibroDict(TypedDict):
    id: int
    titulo: str
    autor: str
    isbn: str
```

### 6. Protocol (Interfaces Estructurales)

```python
from typing import Protocol

class Prestable(Protocol):
    def esta_disponible(self) -> bool: ...
    def prestar(self) -> None: ...
    def devolver(self) -> None: ...

# Cualquier clase que implemente estos métodos es Prestable
def prestar_item(item: Prestable) -> None:
    if item.esta_disponible():
        item.prestar()
```

### 7. Generic Types

```python
from typing import TypeVar, Generic

T = TypeVar("T")

def primer_elemento(items: list[T]) -> T | None:
    return items[0] if items else None

class Caja(Generic[T]):
    def __init__(self, contenido: T):
        self._contenido = contenido

    def obtener(self) -> T:
        return self._contenido
```

### 8. Callable

```python
from typing import Callable

def filtrar(
    items: list[T],
    predicado: Callable[[T], bool]
) -> list[T]:
    return [item for item in items if predicado(item)]
```

### 9. Overload

```python
from typing import overload, Literal

@overload
def buscar(criterio: str, *, por_titulo: Literal[True]) -> list[Libro]: ...

@overload
def buscar(criterio: str, *, por_isbn: Literal[True]) -> Libro | None: ...

def buscar(criterio: str, **kwargs):
    # Implementación real
    ...
```

## Configuración de Herramientas

### mypy (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true
no_implicit_optional = true
strict_equality = true
```

### ruff (pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "ANN", # annotations
    "B",   # bugbear
]
ignore = ["ANN101", "ANN102"]  # self y cls
```

### black (pyproject.toml)

```toml
[tool.black]
line-length = 100
target-version = ['py312']
```

### isort (pyproject.toml)

```toml
[tool.isort]
profile = "black"
line_length = 100
```

## Integración Continua (CI)

Ejemplo de configuración para GitHub Actions:

**.github/workflows/quality.yml:**
```yaml
name: Quality Checks

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Run ruff
        run: poetry run ruff check .

      - name: Run mypy
        run: poetry run mypy biblioteca_tipada.py

      - name: Run black
        run: poetry run black --check .

      - name: Run isort
        run: poetry run isort --check .
```

## Comparación: Con y Sin Type Hints

### Sin Type Hints

```python
def procesar_libro(libro):
    if libro.esta_disponible():
        return libro.prestar()
    return None
```

**Problemas:**
- No se sabe qué tipo es `libro`
- No se sabe qué retorna la función
- IDE no puede ayudar con autocompletado
- Errores solo se descubren en runtime

### Con Type Hints

```python
def procesar_libro(libro: Libro) -> bool:
    if libro.esta_disponible():
        libro.prestar()
        return True
    return False
```

**Ventajas:**
- Tipo de `libro` es claro
- Retorno es explícito
- IDE ofrece autocompletado
- mypy detecta errores antes de ejecutar

## Límites del Tipado Estático

### 1. Duck Typing Dinámico

```python
# mypy no puede verificar esto completamente
def procesar(obj):
    return obj.metodo_dinamico()
```

**Solución:** Usar Protocol

```python
class Procesable(Protocol):
    def metodo_dinamico(self) -> str: ...

def procesar(obj: Procesable) -> str:
    return obj.metodo_dinamico()
```

### 2. Metaprogramación

```python
# mypy no puede seguir esto
MiClase = type("MiClase", (), {"atributo": 42})
```

**Solución:** Evitar cuando sea posible, o usar `cast`

```python
from typing import cast

MiClase = cast(type, type("MiClase", (), {"atributo": 42}))
```

### 3. Monkey Patching

```python
# mypy no detecta esto
import json
json.dumps = lambda x: "modificado"
```

**Solución:** No hacer monkey patching (principio de diseño)

## Ejercicios Propuestos

### Ejercicio 1: Agregar Reservas
Implementa un sistema de reservas de libros con:
- TypedDict para `ReservaDict`
- Clase `Reserva` con type hints completos
- Método `reservar_libro()` en la clase `Biblioteca`

### Ejercicio 2: Sistema de Multas
Crea un módulo para calcular multas con:
- Protocol `Multable`
- Función genérica para calcular multas
- Type hints para diferentes tipos de multas

### Ejercicio 3: Exportar a JSON
Implementa funciones para exportar/importar con:
- TypedDict para estructuras JSON
- Validación de tipos en la importación
- Overload para diferentes formatos

### Ejercicio 4: Tests con Tipos
Crea tests usando pytest con:
- Type hints en las funciones de test
- Fixtures tipadas
- Parametrización con tipos

## Comandos de Referencia Rápida

```bash
# Verificar tipos
poetry run mypy biblioteca_tipada.py

# Verificar calidad
poetry run ruff check .

# Formatear código
poetry run ruff format .
poetry run black .
poetry run isort .

# Ejecutar programa
python biblioteca_tipada.py

# Pre-commit
pre-commit run --all-files

# Todo de una vez
poetry run ruff check --fix . && \
poetry run ruff format . && \
poetry run mypy biblioteca_tipada.py && \
python biblioteca_tipada.py
```

## Recursos Adicionales

- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 526 - Variable Annotations](https://peps.python.org/pep-0526/)
- [PEP 544 - Protocols](https://peps.python.org/pep-0544/)
- [PEP 585 - Type Hinting Generics](https://peps.python.org/pep-0585/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [Python Type Checking Guide](https://realpython.com/python-type-checking/)

## Puntos Clave

1. **Type hints son opcionales pero recomendados** para código de producción
2. **mypy detecta errores antes de ejecutar** el código
3. **Protocols permiten duck typing con tipos** (structural subtyping)
4. **TypedDict es ideal para APIs y JSON** con estructura conocida
5. **Union types (|) son más claros** que Optional en Python 3.10+
6. **Pre-commit hooks mantienen calidad** automáticamente
7. **ruff es más rápido** que flake8 + isort + pyupgrade combinados
8. **Configuración en pyproject.toml** centraliza todas las herramientas

El tipado estático mejora significativamente la mantenibilidad y robustez del código Python.
