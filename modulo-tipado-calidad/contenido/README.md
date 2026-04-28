# Módulo 5: Tipado Estático Opcional y Calidad de Código

## Tabla de Contenidos

1. [Introducción al Tipado Estático en Python](#1-introducción-al-tipado-estático-en-python)
2. [Type Hints Básicos](#2-type-hints-básicos)
3. [Typing Avanzado](#3-typing-avanzado)
4. [Verificadores de Tipos: mypy y pyright](#4-verificadores-de-tipos-mypy-y-pyright)
5. [Límites del Tipado Dinámico](#5-límites-del-tipado-dinámico)
6. [PEP 8: Guía de Estilo](#6-pep-8-guía-de-estilo)
7. [PEP 20: Zen de Python](#7-pep-20-zen-de-python)
8. [Herramientas de Calidad](#8-herramientas-de-calidad)
9. [Pre-commit Hooks](#9-pre-commit-hooks)
10. [Integración Continua (CI)](#10-integración-continua-ci)

---

## 1. Introducción al Tipado Estático en Python

### ¿Qué es el Tipado Estático Opcional?

Python es un lenguaje **dinámicamente tipado**, lo que significa que los tipos se determinan en tiempo de ejecución. Sin embargo, desde Python 3.5 (PEP 484), se introdujo el **tipado estático opcional** mediante type hints.

**Características:**
- **Opcional**: No es obligatorio usar type hints
- **No afecta la ejecución**: Python ignora los tipos en runtime
- **Verificación estática**: Herramientas externas (mypy, pyright) analizan el código sin ejecutarlo
- **Mejora la documentación**: El código es más legible y autodocumentado

### Ventajas del Tipado Estático

```python
# Sin type hints
def calcular_descuento(precio, porcentaje):
    return precio * (1 - porcentaje / 100)

# Con type hints
def calcular_descuento(precio: float, porcentaje: float) -> float:
    return precio * (1 - porcentaje / 100)
```

**Beneficios:**
1. **Detección temprana de errores**: Encontrar bugs antes de ejecutar
2. **Mejor autocompletado en IDEs**: Sugerencias más precisas
3. **Documentación viva**: Los tipos documentan el código
4. **Refactorización segura**: Cambios con mayor confianza
5. **Onboarding más rápido**: Nuevos desarrolladores entienden mejor el código

---

## 2. Type Hints Básicos

### Tipos Primitivos

```python
# Tipos básicos
edad: int = 30
precio: float = 19.99
nombre: str = "Python"
activo: bool = True
nada: None = None

# Funciones con tipos
def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"

def sumar(a: int, b: int) -> int:
    return a + b

# Sin retorno
def imprimir_mensaje(mensaje: str) -> None:
    print(mensaje)
```

### Colecciones

```python
from typing import List, Dict, Set, Tuple

# Listas
numeros: list[int] = [1, 2, 3, 4, 5]
nombres: list[str] = ["Ana", "Juan", "María"]

# Diccionarios
edades: dict[str, int] = {"Ana": 25, "Juan": 30}
configuracion: dict[str, str | int] = {"host": "localhost", "port": 8080}

# Sets
etiquetas: set[str] = {"python", "typing", "quality"}

# Tuplas (tamaño fijo)
coordenadas: tuple[float, float] = (10.5, 20.3)
registro: tuple[int, str, bool] = (1, "activo", True)

# Tuplas de longitud variable
valores: tuple[int, ...] = (1, 2, 3, 4, 5)
```

### Sintaxis Moderna (Python 3.9+)

Desde Python 3.9, se pueden usar los tipos nativos directamente:

```python
# Python 3.9+
def procesar_datos(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Python 3.5-3.8 (necesita typing)
from typing import List, Dict

def procesar_datos(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}
```

---

## 3. Typing Avanzado

### Union Types

Permite que una variable tenga múltiples tipos posibles:

```python
from typing import Union

# Sintaxis con Union
def procesar(valor: Union[int, str]) -> str:
    if isinstance(valor, int):
        return f"Número: {valor}"
    return f"Texto: {valor}"

# Sintaxis moderna con | (Python 3.10+)
def procesar(valor: int | str) -> str:
    if isinstance(valor, int):
        return f"Número: {valor}"
    return f"Texto: {valor}"

# Optional es equivalente a Union[T, None]
from typing import Optional

def buscar_usuario(user_id: int) -> Optional[str]:
    if user_id > 0:
        return f"Usuario {user_id}"
    return None

# Sintaxis moderna
def buscar_usuario(user_id: int) -> str | None:
    if user_id > 0:
        return f"Usuario {user_id}"
    return None
```

### Literal Types

Restringe valores a un conjunto específico de literales:

```python
from typing import Literal

# Solo acepta estos valores exactos
def configurar_modo(modo: Literal["desarrollo", "produccion", "pruebas"]) -> None:
    print(f"Modo: {modo}")

configurar_modo("desarrollo")  # ✓ OK
configurar_modo("staging")     # ✗ Error en mypy

# Literal con múltiples tipos
EstadoPedido = Literal["pendiente", "procesando", "enviado", "entregado"]

def actualizar_estado(estado: EstadoPedido) -> None:
    print(f"Estado: {estado}")

# Combinado con Union
ResultadoAPI = Literal["success", "error", "timeout"]

def procesar_respuesta(resultado: ResultadoAPI) -> bool:
    return resultado == "success"
```

### TypedDict

Define diccionarios con estructura específica:

```python
from typing import TypedDict

# Definición básica
class Usuario(TypedDict):
    id: int
    nombre: str
    email: str
    activo: bool

# Uso
usuario: Usuario = {
    "id": 1,
    "nombre": "Ana García",
    "email": "ana@example.com",
    "activo": True,
}

# Campos opcionales
class UsuarioOpcional(TypedDict, total=False):
    id: int
    nombre: str
    telefono: str  # Opcional
    direccion: str  # Opcional

# Con Required y NotRequired (Python 3.11+)
from typing import Required, NotRequired

class Producto(TypedDict):
    id: Required[int]
    nombre: Required[str]
    descripcion: NotRequired[str]
    precio: Required[float]

# Herencia
class UsuarioBase(TypedDict):
    id: int
    nombre: str

class UsuarioCompleto(UsuarioBase):
    email: str
    telefono: str
```

### Protocol

Define interfaces estructurales (duck typing con tipos):

```python
from typing import Protocol

# Definir un protocolo
class Comparable(Protocol):
    def __lt__(self, other: "Comparable") -> bool: ...
    def __gt__(self, other: "Comparable") -> bool: ...

# Cualquier clase que implemente estos métodos es Comparable
class Persona:
    def __init__(self, edad: int):
        self.edad = edad

    def __lt__(self, other: "Persona") -> bool:
        return self.edad < other.edad

    def __gt__(self, other: "Persona") -> bool:
        return self.edad > other.edad

# Función que acepta cualquier Comparable
def ordenar_items(items: list[Comparable]) -> list[Comparable]:
    return sorted(items)

# Funciona con Persona aunque no hereda de Comparable
personas = [Persona(25), Persona(30), Persona(20)]
ordenadas = ordenar_items(personas)  # ✓ OK

# Protocolo más complejo
class Persistible(Protocol):
    def save(self) -> None: ...
    def delete(self) -> None: ...
    def load(self, id: int) -> None: ...

class Usuario:
    def save(self) -> None:
        print("Guardando usuario...")

    def delete(self) -> None:
        print("Eliminando usuario...")

    def load(self, id: int) -> None:
        print(f"Cargando usuario {id}...")

def guardar_entidad(entidad: Persistible) -> None:
    entidad.save()

usuario = Usuario()
guardar_entidad(usuario)  # ✓ OK
```

### Generic Types

Crear tipos genéricos reutilizables:

```python
from typing import TypeVar, Generic

# TypeVar simple
T = TypeVar("T")

def primer_elemento(items: list[T]) -> T | None:
    return items[0] if items else None

# Inferencia de tipos
numeros = [1, 2, 3]
primero = primer_elemento(numeros)  # tipo: int | None

# Clase genérica
class Caja(Generic[T]):
    def __init__(self, contenido: T):
        self._contenido = contenido

    def obtener(self) -> T:
        return self._contenido

    def actualizar(self, nuevo: T) -> None:
        self._contenido = nuevo

# Uso
caja_int: Caja[int] = Caja(42)
caja_str: Caja[str] = Caja("Python")

numero = caja_int.obtener()  # tipo: int
texto = caja_str.obtener()   # tipo: str

# TypeVar con restricciones
NumeroType = TypeVar("NumeroType", int, float)

def sumar(a: NumeroType, b: NumeroType) -> NumeroType:
    return a + b  # type: ignore

# TypeVar con bound
from typing import Protocol

class Sumable(Protocol):
    def __add__(self, other: "Sumable") -> "Sumable": ...

SumableT = TypeVar("SumableT", bound=Sumable)

def sumar_todos(items: list[SumableT]) -> SumableT:
    resultado = items[0]
    for item in items[1:]:
        resultado = resultado + item  # type: ignore
    return resultado
```

### Callable

Tipos para funciones y callables:

```python
from typing import Callable

# Función que acepta un callable
def aplicar_operacion(
    valor: int,
    operacion: Callable[[int], int]
) -> int:
    return operacion(valor)

def duplicar(x: int) -> int:
    return x * 2

resultado = aplicar_operacion(5, duplicar)  # 10

# Callable con múltiples argumentos
def procesar_lista(
    items: list[int],
    transformar: Callable[[int, int], int]
) -> list[int]:
    resultado = []
    for i, item in enumerate(items):
        resultado.append(transformar(i, item))
    return resultado

# Callable que retorna None
def ejecutar_callbacks(callbacks: list[Callable[[], None]]) -> None:
    for callback in callbacks:
        callback()

# Callable genérico
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")

def mapear(items: list[T], fn: Callable[[T], R]) -> list[R]:
    return [fn(item) for item in items]
```

### Type Aliases

Crear alias para tipos complejos:

```python
from typing import TypeAlias

# Alias simple
UserID: TypeAlias = int
Username: TypeAlias = str

def obtener_usuario(user_id: UserID) -> Username:
    return f"usuario_{user_id}"

# Alias complejos
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

ConfigDict: TypeAlias = dict[str, str | int | bool]

# Alias con genéricos
from typing import TypeVar

T = TypeVar("T")
ListaOpcional: TypeAlias = list[T] | None

def procesar(items: ListaOpcional[int]) -> int:
    if items is None:
        return 0
    return sum(items)
```

### Tipos Especiales

```python
from typing import Any, NoReturn, Never, Final, ClassVar

# Any: acepta cualquier tipo (evitar cuando sea posible)
def procesar_cualquier_cosa(valor: Any) -> Any:
    return valor

# NoReturn: función que nunca retorna
def lanzar_error() -> NoReturn:
    raise RuntimeError("Error fatal")

# Never (Python 3.11+): código inalcanzable
def assert_never(value: Never) -> Never:
    raise AssertionError(f"Valor inesperado: {value}")

# Final: valor que no debe cambiar
PI: Final = 3.14159
PI = 3.14  # ✗ Error en mypy

# ClassVar: variable de clase
from dataclasses import dataclass

@dataclass
class Configuracion:
    host: str
    port: int
    max_conexiones: ClassVar[int] = 100  # Variable de clase
```

---

## 4. Verificadores de Tipos: mypy y pyright

### mypy

**mypy** es el verificador de tipos oficial de Python.

**Instalación:**
```bash
pip install mypy
```

**Uso básico:**
```bash
# Verificar un archivo
mypy archivo.py

# Verificar un directorio
mypy src/

# Modo estricto
mypy --strict archivo.py

# Generar reporte HTML
mypy --html-report mypy-report src/
```

**Configuración (mypy.ini o pyproject.toml):**
```ini
[mypy]
python_version = 3.12
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_unimported = False
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
check_untyped_defs = True
strict_equality = True

# Ignorar módulos sin tipos
[mypy-requests.*]
ignore_missing_imports = True
```

**pyproject.toml:**
```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### pyright

**pyright** es un verificador de tipos desarrollado por Microsoft, extremadamente rápido.

**Instalación:**
```bash
npm install -g pyright
# o
pip install pyright
```

**Uso:**
```bash
# Verificar un archivo
pyright archivo.py

# Verificar un proyecto
pyright

# Con configuración específica
pyright --project pyproject.toml
```

**Configuración (pyrightconfig.json o pyproject.toml):**
```json
{
  "pythonVersion": "3.12",
  "typeCheckingMode": "strict",
  "reportUnusedImport": true,
  "reportUnusedVariable": true,
  "reportDuplicateImport": true
}
```

**pyproject.toml:**
```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
reportUnusedImport = true
reportUnusedVariable = true
```

### Comparación mypy vs pyright

| Característica | mypy | pyright |
|----------------|------|---------|
| Velocidad | Moderada | Muy rápida |
| Configuración | Flexible | Simple |
| Integración IDE | Buena | Excelente (VS Code) |
| Comunidad | Más grande | Creciente |
| Strictness | Configurable | Muy estricto |

---

## 5. Límites del Tipado Dinámico

### Casos Problemáticos

```python
# 1. Tipos dinámicos en runtime
def procesar(valor):
    if isinstance(valor, int):
        return valor * 2
    elif isinstance(valor, str):
        return valor.upper()
    else:
        return None

# mypy no puede inferir el tipo de retorno exacto
# Retorno: int | str | None

# 2. Duck typing
class Pato:
    def hablar(self) -> str:
        return "Cuac"

class Perro:
    def hablar(self) -> str:
        return "Guau"

def hacer_hablar(animal):  # Tipo desconocido
    return animal.hablar()

# 3. Metaprogramación
def crear_clase_dinamica(nombre: str):
    return type(nombre, (), {"metodo": lambda self: "hola"})

MiClase = crear_clase_dinamica("MiClase")
# mypy no puede verificar el tipo de MiClase

# 4. Monkey patching
import json

def custom_dumps(obj):
    return "custom"

json.dumps = custom_dumps  # mypy no detecta esto
```

### Soluciones y Workarounds

```python
from typing import cast, TYPE_CHECKING, overload

# 1. Type narrowing con isinstance
def procesar(valor: int | str | None) -> int | str | None:
    if isinstance(valor, int):
        return valor * 2  # mypy sabe que es int aquí
    elif isinstance(valor, str):
        return valor.upper()  # mypy sabe que es str aquí
    return None

# 2. Protocol para duck typing
from typing import Protocol

class Hablable(Protocol):
    def hablar(self) -> str: ...

def hacer_hablar(animal: Hablable) -> str:
    return animal.hablar()

# 3. cast para conversiones forzadas
from typing import cast

def obtener_config() -> dict:
    return {"clave": "valor"}

config = cast(dict[str, str], obtener_config())

# 4. overload para múltiples signatures
from typing import overload

@overload
def procesar(valor: int) -> int: ...

@overload
def procesar(valor: str) -> str: ...

def procesar(valor: int | str) -> int | str:
    if isinstance(valor, int):
        return valor * 2
    return valor.upper()

# 5. TYPE_CHECKING para imports solo de tipos
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modulo_pesado import ClaseGrande

def procesar(obj: "ClaseGrande") -> None:
    pass
```

---

## 6. PEP 8: Guía de Estilo

### Reglas Principales

**Indentación:**
```python
# ✓ Correcto: 4 espacios
def funcion():
    if condicion:
        hacer_algo()

# ✗ Incorrecto: 2 espacios o tabs
def funcion():
  if condicion:
    hacer_algo()
```

**Longitud de línea:**
```python
# ✓ Máximo 79 caracteres para código
def funcion_con_nombre_largo(
    parametro_uno: int,
    parametro_dos: str,
) -> bool:
    return True

# ✓ Máximo 72 para comentarios y docstrings
```

**Imports:**
```python
# ✓ Orden correcto
# 1. Librería estándar
import os
import sys
from pathlib import Path

# 2. Librerías de terceros
import requests
from flask import Flask

# 3. Imports locales
from myapp import models
from myapp.utils import helper

# ✗ Incorrecto
from flask import Flask
import os  # debería estar antes
```

**Espacios en blanco:**
```python
# ✓ Correcto
spam(ham[1], {eggs: 2})
x = 1
y = 2
long_variable = 3

if x == 4:
    print(x, y)

# ✗ Incorrecto
spam( ham[ 1 ], { eggs: 2 } )
x             = 1
y             = 2
long_variable = 3

if x == 4 : print(x , y)
```

**Nombres:**
```python
# ✓ Variables y funciones: snake_case
mi_variable = 10
def mi_funcion():
    pass

# ✓ Clases: PascalCase
class MiClase:
    pass

# ✓ Constantes: UPPER_CASE
MAX_CONEXIONES = 100
API_KEY = "secret"

# ✓ Métodos privados: _prefijo
class MiClase:
    def _metodo_interno(self):
        pass
```

---

## 7. PEP 20: Zen de Python

```python
import this
```

**Principios clave:**

1. **Bello es mejor que feo**
```python
# ✓ Bello
usuarios_activos = [u for u in usuarios if u.activo]

# ✗ Feo
usuarios_activos=list(filter(lambda u:u.activo,usuarios))
```

2. **Explícito es mejor que implícito**
```python
# ✓ Explícito
def calcular_total(precio: float, impuesto: float) -> float:
    return precio + (precio * impuesto)

# ✗ Implícito
def calc(p, i):
    return p + p * i
```

3. **Simple es mejor que complejo**
```python
# ✓ Simple
if usuario and usuario.activo:
    procesar(usuario)

# ✗ Complejo
if usuario is not None and hasattr(usuario, 'activo') and usuario.activo is True:
    procesar(usuario)
```

4. **Legibilidad cuenta**
```python
# ✓ Legible
SEGUNDOS_POR_DIA = 60 * 60 * 24

# ✗ No legible
SPD = 86400
```

---

## 8. Herramientas de Calidad

### ruff

Linter ultra rápido que reemplaza a flake8, isort, y más.

```bash
# Instalación
pip install ruff

# Uso
ruff check .                    # Verificar
ruff check --fix .              # Corregir automáticamente
ruff format .                   # Formatear código
```

**Configuración (pyproject.toml):**
```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "ANN", # annotations
    "B",   # bugbear
    "C4",  # comprehensions
]
ignore = ["ANN101"]  # Ignorar self: Self

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ANN"]  # No requerir anotaciones en tests
```

### black

Formateador de código opinionado.

```bash
pip install black

black .                  # Formatear todo
black --check .          # Solo verificar
black --diff archivo.py  # Mostrar cambios
```

**Configuración:**
```toml
[tool.black]
line-length = 100
target-version = ['py312']
include = '\.pyi?$'
```

### isort

Ordena imports automáticamente.

```bash
pip install isort

isort .                  # Ordenar imports
isort --check .          # Solo verificar
```

**Configuración:**
```toml
[tool.isort]
profile = "black"
line_length = 100
```

---

## 9. Pre-commit Hooks

### Configuración

**Instalación:**
```bash
pip install pre-commit
```

**Archivo .pre-commit-config.yaml:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-toml

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.11
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

**Activar:**
```bash
pre-commit install
```

---

## 10. Integración Continua (CI)

### GitHub Actions

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
        run: poetry run mypy src/

      - name: Run black
        run: poetry run black --check .

      - name: Run isort
        run: poetry run isort --check .
```

### GitLab CI

**.gitlab-ci.yml:**
```yaml
stages:
  - quality

quality_checks:
  stage: quality
  image: python:3.12
  script:
    - pip install poetry
    - poetry install
    - poetry run ruff check .
    - poetry run mypy src/
    - poetry run black --check .
    - poetry run isort --check .
```

---

## Resumen

- **Type hints**: Documentan y validan tipos sin afectar runtime
- **Typing avanzado**: Union, Literal, TypedDict, Protocol, Generic
- **mypy/pyright**: Verificación estática de tipos
- **PEP 8**: Guía de estilo estándar de Python
- **PEP 20**: Principios de diseño (Zen de Python)
- **ruff/black/isort**: Herramientas modernas de calidad
- **Pre-commit**: Verificaciones automáticas antes de commit
- **CI**: Integración continua para mantener calidad

El tipado estático y las herramientas de calidad mejoran significativamente la mantenibilidad, legibilidad y robustez del código Python.
