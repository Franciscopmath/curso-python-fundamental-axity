# Módulo: Entorno y Herramientas

## Contenidos Clave

### 1. Instalación de Python 3.12

Python 3.12 es la versión más reciente del lenguaje (al momento de este curso). Trae mejoras significativas:

**Características principales:**
- Mejor rendimiento (hasta 5% más rápido que 3.11)
- Mensajes de error más descriptivos
- Mejoras en el sistema de tipos
- Nuevas funcionalidades en f-strings
- Mejor soporte para concurrencia

**Instalación con pyenv (recomendado):**

pyenv permite gestionar múltiples versiones de Python sin afectar el sistema.

```bash
# Instalar pyenv
curl https://pyenv.run | bash

# Configurar en ~/.bashrc o ~/.bash_profile
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

# Instalar Python 3.12
pyenv install 3.12.0

# Establecer como versión global o local
pyenv global 3.12.0  # Global para todo el sistema
pyenv local 3.12.0   # Solo para el directorio actual
```

### 2. Ambientes Virtuales y Poetry

#### Ambientes Virtuales

Un ambiente virtual aísla las dependencias de cada proyecto, evitando conflictos.

**Beneficios:**
- Independencia entre proyectos
- Reproducibilidad del entorno
- Evita contaminación del Python del sistema
- Facilita el despliegue

**Métodos tradicionales:**
```bash
# Con venv (integrado en Python)
python -m venv mi_entorno
source mi_entorno/bin/activate  # Linux/Mac
```

#### Poetry - Gestor Moderno de Dependencias

Poetry es la herramienta recomendada por Axity para gestión de proyectos Python.

**Ventajas sobre pip tradicional:**
- Gestión automática de dependencias
- Archivo único de configuración (pyproject.toml)
- Resolución inteligente de conflictos
- Publicación de paquetes simplificada
- Ambientes virtuales integrados

**Instalación:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Comandos básicos:**
```bash
poetry new mi_proyecto          # Crear proyecto nuevo
poetry init                     # Inicializar en proyecto existente
poetry add paquete             # Añadir dependencia
poetry add --group dev paquete # Dependencia de desarrollo
poetry install                 # Instalar todas las dependencias
poetry update                  # Actualizar dependencias
poetry shell                   # Activar ambiente virtual
poetry run python script.py    # Ejecutar script en el ambiente
```

### 3. IDEs - Entornos de Desarrollo

#### PyCharm

IDE especializado en Python desarrollado por JetBrains.

**Ventajas:**
- Autocompletado inteligente
- Depurador integrado potente
- Refactorización avanzada
- Integración con bases de datos
- Soporte para frameworks (Django, FastAPI, Flask)

**Versiones:**
- Professional (pago, más completa)
- Community (gratuita, suficiente para aprender)

**Extensiones útiles:**
- IdeaVim (para usuarios de Vim)
- Rainbow Brackets
- Key Promoter X (aprender atajos)

#### Visual Studio Code (Recomendado)

Editor ligero y extensible, recomendado por el instructor.

**Ventajas:**
- Gratuito y open source
- Muy ligero y rápido
- Ecosistema extenso de extensiones
- Integración con Git
- Terminal integrada
- Soporte para múltiples lenguajes

**Extensiones esenciales para Python:**

1. **Python (Microsoft)** - Básica, debe instalarse primero
2. **Pylance** - IntelliSense avanzado
3. **Python Debugger** - Depuración
4. **Black Formatter** - Formateo automático
5. **isort** - Ordenamiento de imports
6. **Ruff** - Linter ultra rápido
7. **autoDocstring** - Generación de docstrings
8. **Python Test Explorer** - Visualización de tests
9. **GitLens** - Mejor integración con Git
10. **Error Lens** - Muestra errores inline

**Extensión Polux Code Assistant:**
- Herramienta interna de Axity
- Basada en IA para acelerar desarrollo
- Solicitar acceso a través de Cindy/Roserío

### 4. Estructura de Proyecto

#### pyproject.toml

Archivo estándar moderno para configuración de proyectos Python (PEP 518).

**Estructura típica:**

```toml
[tool.poetry]
name = "mi-proyecto"
version = "0.1.0"
description = "Descripción del proyecto"
authors = ["Tu Nombre <tu@email.com>"]
readme = "README.md"
license = "MIT"

[tool.poetry.dependencies]
python = "^3.12"
fastapi = "^0.104.0"
uvicorn = "^0.24.0"

[tool.poetry.group.dev.dependencies]
black = "^23.11.0"
isort = "^5.12.0"
ruff = "^0.1.6"
pre-commit = "^3.5.0"
pytest = "^7.4.3"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Secciones importantes:**
- `[tool.poetry]`: Metadatos del proyecto
- `[tool.poetry.dependencies]`: Dependencias de producción
- `[tool.poetry.group.dev.dependencies]`: Dependencias de desarrollo
- `[build-system]`: Sistema de build

#### requirements.txt (Método tradicional)

Archivo de texto con lista de paquetes. Poetry puede generarlo:

```bash
poetry export -f requirements.txt --output requirements.txt
```

**Diferencias:**
- `pyproject.toml`: Más moderno, versátil, soporta rangos de versiones
- `requirements.txt`: Tradicional, versiones fijas, más simple

### 5. PEP 8 - Guía de Estilo

PEP 8 es la guía oficial de estilo para código Python.

**Principios fundamentales:**

#### Nombres de variables y funciones
```python
# Correcto - snake_case
nombre_usuario = "Francisco"
def calcular_total(precio, cantidad):
    pass

# Incorrecto - camelCase
nombreUsuario = "Francisco"
def calcularTotal(precio, cantidad):
    pass
```

#### Nombres de clases
```python
# Correcto - PascalCase
class UsuarioManager:
    pass

# Incorrecto
class usuario_manager:
    pass
```

#### Constantes
```python
# Correcto - UPPERCASE
MAX_CONEXIONES = 100
API_URL = "https://api.ejemplo.com"
```

#### Indentación
```python
# Correcto - 4 espacios
def funcion():
    if condicion:
        hacer_algo()
```

#### Longitud de línea
- Máximo 79 caracteres por línea
- 72 para comentarios y docstrings

#### Imports
```python
# Correcto - orden específico
import os
import sys

from typing import List, Dict

import numpy as np
import pandas as pd

from mi_paquete import modulo
```

#### Espacios en blanco
```python
# Correcto
funcion(arg1, arg2)
lista[indice]
x = y + 1

# Incorrecto
funcion( arg1 , arg2 )
lista [indice]
x=y+1
```

### 6. PEP 20 - Zen de Python

Filosofía de diseño de Python. Ver con: `import this`

**Principios clave:**

1. **Bello es mejor que feo** - Código legible y estético
2. **Explícito es mejor que implícito** - Claridad sobre cleverness
3. **Simple es mejor que complejo** - Evitar sobre-ingeniería
4. **Complejo es mejor que complicado** - Si es necesario, hazlo bien
5. **Plano es mejor que anidado** - Evitar indentación excesiva
6. **Espaciado importa** - Legibilidad
7. **Casos especiales no son tan especiales** - Consistencia
8. **Los errores nunca deben pasar silenciosamente** - Manejo explícito
9. **Ante la ambigüedad, rechaza la tentación de adivinar** - Ser explícito
10. **Debe haber una -y preferiblemente solo una- forma obvia de hacerlo**

**Aplicación práctica:**

```python
# Explícito es mejor que implícito
# Bueno
def obtener_usuarios_activos(usuarios: List[Usuario]) -> List[Usuario]:
    return [u for u in usuarios if u.activo]

# Malo (demasiado implícito)
def get_users(u):
    return [x for x in u if x.a]
```

### 7. Herramientas de Calidad de Código

#### Black - Formateador Automático

"The uncompromising code formatter"

**Características:**
- Formateo automático sin configuración
- Estilo consistente y determinista
- Ahorra tiempo en discusiones de estilo

**Uso:**
```bash
poetry add --group dev black
black mi_archivo.py
black .  # Formatear todo el proyecto
```

**Configuración en pyproject.toml:**
```toml
[tool.black]
line-length = 88
target-version = ['py312']
include = '\.pyi?$'
```

#### isort - Ordenamiento de Imports

Organiza automáticamente los imports según PEP 8.

**Uso:**
```bash
poetry add --group dev isort
isort mi_archivo.py
isort .
```

**Configuración en pyproject.toml:**
```toml
[tool.isort]
profile = "black"  # Compatibilidad con Black
line_length = 88
```

#### Ruff - Linter Ultra Rápido

Linter moderno escrito en Rust, 10-100x más rápido que flake8.

**Características:**
- Combina funcionalidad de flake8, pylint, pyupgrade, etc.
- Extremadamente rápido
- Autofix para muchas reglas

**Uso:**
```bash
poetry add --group dev ruff
ruff check .
ruff check --fix .  # Corregir automáticamente
```

**Configuración en pyproject.toml:**
```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
]
ignore = []
```

#### pre-commit - Automatización de Hooks

Ejecuta herramientas automáticamente antes de cada commit.

**Instalación:**
```bash
poetry add --group dev pre-commit
```

**Archivo `.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
```

**Activación:**
```bash
pre-commit install
```

**Uso:**
- Automático: Se ejecuta en cada `git commit`
- Manual: `pre-commit run --all-files`

## Objetivos del Módulo

Al completar este módulo deberás ser capaz de:

1. Instalar y gestionar versiones de Python con pyenv
2. Crear y gestionar proyectos con Poetry
3. Configurar un IDE (VS Code o PyCharm) con extensiones útiles
4. Aplicar PEP 8 en tu código
5. Comprender y aplicar los principios del Zen de Python (PEP 20)
6. Utilizar black, isort y ruff para mantener calidad de código
7. Configurar pre-commit hooks para automatizar verificaciones
8. Documentar excepciones locales a PEP 8 cuando sea necesario

## Recursos Adicionales

- [Documentación oficial de Python 3.12](https://docs.python.org/3.12/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [PEP 8](https://peps.python.org/pep-0008/)
- [PEP 20 - Zen of Python](https://peps.python.org/pep-0020/)
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)

## Notas Importantes

- Seguir el stack tecnológico de Axity (evitar desviarse hacia otros frameworks)
- Utilizar IA (Polux One, ChatGPT, etc.) para **aprender**, no solo para copiar código
- Enfocarse en principios y patrones, son agnósticos al lenguaje
- La arquitectura hexagonal se verá en módulos posteriores
- Guardar cada laboratorio en carpetas separadas dentro del módulo
