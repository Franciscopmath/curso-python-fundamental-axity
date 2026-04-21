# Curso Python - Fundamental Level

Repositorio del curso de Python organizado por módulos con arquitectura hexagonal.

## Estructura del Proyecto

```
fundamental-level/
├── modulo-entorno-herramientas/
│   ├── contenido/
│   │   └── README.md          # Documentación teórica del módulo
│   └── laboratorio/
│       ├── pyproject.toml     # Configuración Poetry y herramientas
│       ├── .pre-commit-config.yaml
│       ├── codigo_malo.py     # Código con violaciones PEP 8
│       ├── codigo_corregido.py
│       ├── README.md
│       └── INSTRUCCIONES_INSTALACION.md
├── modulo-fundamentos-lenguaje/
│   ├── contenido/
│   │   └── README.md          # Documentación teórica completa
│   └── laboratorio/
│       ├── pyproject.toml     # Configuración Poetry
│       ├── procesador_productos.py  # Script principal
│       ├── productos.json     # Datos de ejemplo
│       └── README.md          # Instrucciones del laboratorio
├── .gitignore
└── README.md                   # Este archivo
```

## Módulos Completados

### ✅ Módulo: Entorno y Herramientas

**Contenidos cubiertos:**
- Instalación de Python 3.12 con pyenv
- Gestión de ambientes virtuales con Poetry
- Configuración de IDEs (VS Code, PyCharm)
- Estructura de proyectos (pyproject.toml)
- PEP 8 - Guía de estilo
- PEP 20 - Zen de Python
- Herramientas de calidad: black, isort, ruff
- Pre-commit hooks

**Laboratorio implementado:**
- Proyecto completo con Poetry
- Configuración de todas las herramientas
- Ejemplos de código con/sin violaciones PEP 8
- Demostración de corrección automática

**Ubicación:** [modulo-entorno-herramientas/](modulo-entorno-herramientas/)

### ✅ Módulo 2: Fundamentos del Lenguaje

**Contenidos cubiertos:**
- Sintaxis e indentación
- Variables y alcance (LEGB)
- Tipos básicos: int, float, str, bool, None
- Colecciones: list, dict, set, tuple
- Control de flujo: if, for, while, comprehensions
- Errores y excepciones (try-except-finally)
- Expresiones regulares (re)
- Argumentos de línea de comandos (argparse)

**Laboratorio implementado:**
- Script de procesamiento de archivos JSON
- Filtrado y agregación de datos de productos
- Manejo robusto de errores de archivo y formato
- Excepciones personalizadas
- CLI con múltiples opciones de filtrado
- Uso de todas las estructuras de datos
- Type hints completos
- 100% PEP 8 compliant

**Ubicación:** [modulo-fundamentos-lenguaje/](modulo-fundamentos-lenguaje/)

## Próximos Módulos

Los siguientes módulos se agregarán a medida que avance el curso:

- Programación Pythonica
- Objetos y modelos de datos
- Tipos estáticos opcionales
- Calidad y testing
- Librerías estándar
- I/O y manejo de archivos
- HTTP y consumo de APIs

## Cómo Usar Este Repositorio

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd fundamental-level
```

### 2. Navegar a un módulo específico

```bash
cd modulo-entorno-herramientas
```

### 3. Leer la documentación teórica

```bash
cat contenido/README.md
```

### 4. Ejecutar el laboratorio

```bash
cd laboratorio

# Instalar dependencias
poetry install

# Ver el código de ejemplo
cat codigo_malo.py
cat codigo_corregido.py

# Ejecutar herramientas
poetry run ruff check codigo_corregido.py
poetry run black codigo_corregido.py
poetry run isort codigo_corregido.py
```

## Requisitos del Sistema

- Python 3.12 (instalado con pyenv)
- Poetry 2.3+
- Git
- pyenv 2.6+

## Instalación Rápida

```bash
# Instalar pyenv
curl https://pyenv.run | bash

# Configurar shell (añadir a ~/.bashrc o ~/.bash_profile)
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

# Instalar Python 3.12
pyenv install 3.12.0

# Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

## Herramientas Utilizadas

| Herramienta | Propósito | Versión |
|-------------|-----------|---------|
| Python | Lenguaje de programación | 3.12.0 |
| pyenv | Gestor de versiones de Python | 2.6+ |
| Poetry | Gestor de dependencias | 2.3+ |
| Black | Formateador de código | 26.3+ |
| isort | Ordenador de imports | 8.0+ |
| Ruff | Linter ultra rápido | 0.15+ |
| pre-commit | Hooks de Git | 4.5+ |
| pytest | Framework de testing | 9.0+ |

## Convenciones del Proyecto

### Estructura de Carpetas

Cada módulo sigue esta estructura:

```
modulo-nombre/
├── contenido/
│   └── README.md      # Teoría e investigación
└── laboratorio/
    ├── README.md      # Instrucciones del laboratorio
    ├── código...      # Implementación práctica
    └── tests/         # Pruebas (si aplica)
```

### Nombres de Archivos

- `codigo_malo.py` - Código con violaciones intencionales
- `codigo_corregido.py` - Código siguiendo mejores prácticas
- `README.md` - Documentación en Markdown
- `pyproject.toml` - Configuración del proyecto

### Estilo de Código

Seguimos estrictamente:
- **PEP 8** para estilo
- **PEP 20** para filosofía
- **Black** para formateo (88 caracteres/línea)
- **Type hints** cuando sea apropiado

## Comandos Útiles

```bash
# Ver estructura del proyecto
tree -L 3 -I '__pycache__|*.pyc|.git'

# Ejecutar todas las herramientas de calidad
cd modulo-entorno-herramientas/laboratorio
poetry run ruff check --fix . && poetry run isort . && poetry run black .

# Verificar ambiente virtual
poetry env info

# Listar dependencias
poetry show
```

## Recursos

- [Documentación oficial de Python 3.12](https://docs.python.org/3.12/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [PEP 8](https://peps.python.org/pep-0008/)
- [PEP 20 - Zen of Python](https://peps.python.org/pep-0020/)
- [Black](https://black.readthedocs.io/)
- [Ruff](https://docs.astral.sh/ruff/)

## Notas

- Este repositorio se actualizará con nuevos módulos a medida que avance el curso
- Cada módulo es independiente y puede estudiarse por separado
- Se recomienda seguir el orden sugerido en el curso
- Los laboratorios son prácticos y deben ejecutarse para mejor comprensión

## Autor

Francisco Math - Curso Python Axity

## Licencia

Material educativo - Uso académico
