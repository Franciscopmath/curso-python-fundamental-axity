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
├── modulo-funciones-pythonic/
│   ├── contenido/
│   │   └── README.md          # Teoría avanzada de funciones
│   └── laboratorio/
│       ├── pyproject.toml     # Configuración Poetry
│       ├── utilidades_pythonic.py  # Decoradores, generadores, context managers
│       └── README.md          # Instrucciones detalladas
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

### ✅ Módulo 3: Funciones y Programación Pythonic

**Contenidos cubiertos:**
- Funciones: argumentos posicionales, nombrados, *args/**kwargs
- Lambdas y funciones anónimas
- Closures y scope de funciones
- Decoradores: simples, con parámetros, preservación de metadata
- Iteradores y protocolo de iteración
- Generadores: yield, yield from, expresiones generadoras
- Comprensiones: list, dict, set
- Context managers: __enter__/__exit__, @contextmanager
- Programación pythonic: idiomas, EAFP, duck typing

**Laboratorio implementado:**
- Decorador de reintentos con backoff exponencial y jitter
- Generador por lotes (batch processing)
- Generador con ventanas deslizantes (windowed)
- Context manager de temporización (3 implementaciones)
- Temporizador acumulativo para benchmarks
- 600+ líneas de código pythonic avanzado
- Type hints completos con TypeVar
- Ejemplos ejecutables de todos los conceptos
- 100% PEP 8 compliant

**Ubicación:** [modulo-funciones-pythonic/](modulo-funciones-pythonic/)

### ✅ Módulo 4: Objetos y Modelos de Datos

**Contenidos cubiertos:**
- Clases: definición, atributos, métodos
- Herencia: simple, múltiple, super(), MRO
- Composición: preferir composición sobre herencia
- Dunder methods: __init__, __str__, __repr__, __eq__, __lt__, __hash__
- Dataclasses: @dataclass, field(), __post_init__
- Attrs: alternativa a dataclasses con más features
- Pydantic: validación y serialización de datos
- Comparación entre dataclasses, attrs y Pydantic

**Laboratorio implementado:**
- Sistema de gestión de pedidos completo
- Dataclass Pedido con propiedades calculadas (subtotal, impuestos, total)
- Métodos de comparación personalizados (__eq__, __lt__, etc.)
- Pydantic models (PedidoIn/PedidoOut) con validación
- Conversión bidireccional Pydantic ↔ Entidades
- Gestión de estado con transiciones válidas
- Uso de Decimal para precisión monetaria
- Enumeraciones (StrEnum) para valores constantes
- 900+ líneas de código con 7 ejemplos ejecutables
- Type hints completos y 100% PEP 8 compliant

**Ubicación:** [modulo-objetos-modelos/](modulo-objetos-modelos/)

### ✅ Módulo 5: Tipado Estático Opcional y Calidad

**Contenidos cubiertos:**
- Type hints básicos: int, str, float, bool, list, dict, set, tuple
- Typing avanzado: Union (|), Literal, TypedDict, Protocol, Generic
- Type aliases con TypeAlias
- Callable types para funciones como parámetros
- Overload para múltiples signatures de funciones
- Verificadores de tipos: mypy y pyright
- Límites del tipado dinámico y soluciones
- PEP 8: guía de estilo de Python
- PEP 20: Zen de Python como guía de diseño
- Herramientas modernas: ruff, black, isort
- Pre-commit hooks para verificaciones automáticas
- Configuración para CI/CD (GitHub Actions, GitLab CI)

**Laboratorio implementado:**
- Sistema de biblioteca completamente tipado (800+ líneas)
- Type hints completos en todas las funciones y métodos
- Union types (|) para valores opcionales
- Literal types para valores específicos
- TypedDict para estructuras de datos JSON
- Protocol para interfaces estructurales (duck typing tipado)
- Generic types con TypeVar para funciones genéricas
- Overload para múltiples signatures
- Configuración completa de mypy, ruff, black, isort
- Pre-commit hooks configurados (.pre-commit-config.yaml)
- 100% PEP 8 compliant (verificado con ruff)
- Listo para integración continua

**Ubicación:** [modulo-tipado-calidad/](modulo-tipado-calidad/)

### ✅ Módulo 6: Librería Estándar y E/S

**Contenidos cubiertos:**
- pathlib: Manejo moderno de rutas y archivos
- CSV: Lectura y escritura de datos tabulares con csv.DictReader/DictWriter
- JSON: Serialización y deserialización con json.load/dump
- YAML: Configuración legible (con pyyaml)
- datetime: Fechas, horas, zonas horarias y cálculos temporales
- logging: Sistema completo con niveles (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- subprocess: Ejecución segura de comandos externos
- Manejo de encodings (UTF-8, Latin-1)
- Context managers (with) para gestión de recursos

**Laboratorio implementado:**
- Procesador de ventas con ingesta de CSV (600+ líneas)
- Lectura de 50 registros de ventas desde CSV
- Cálculo de métricas agregadas (total, promedio, min, max)
- Agregaciones por categoría, región, mes
- Top 10 productos y vendedores
- Exportación completa a JSON con metadata
- Sistema de logging con múltiples niveles
- RotatingFileHandler (10 MB, 5 backups)
- Logging a consola (INFO) y archivo (DEBUG)
- pathlib para manejo de rutas multiplataforma
- Decimal para precisión monetaria
- Filtrado de datos por múltiples criterios
- Dataclasses con properties calculadas
- Type hints completos y 100% PEP 8 compliant

**Ubicación:** [modulo-libreria-estandar/](modulo-libreria-estandar/)

### ✅ Módulo 7: HTTP y Consumo de APIs

**Contenidos cubiertos:**
- HTTP: Métodos (GET, POST, PUT, PATCH, DELETE), códigos de estado (2xx, 3xx, 4xx, 5xx)
- httpx: Cliente HTTP moderno con HTTP/2 y soporte async/await
- Comparación: requests vs httpx vs aiohttp
- Timeouts: connect, read, write, pool (configuración granular)
- Reintentos: backoff exponencial, jitter, estrategias de reintento
- Manejo de errores: TimeoutException, HTTPStatusError, NetworkError
- Streaming: Descarga eficiente de archivos grandes
- Autenticación: Bearer tokens, API keys, OAuth 2.0
- Client reutilizable: Reutilización de conexiones HTTP
- Async/await: Requests concurrentes con AsyncClient
- Buenas prácticas: Context managers, verificación de status, logging

**Laboratorio implementado:**
- 6 ejercicios progresivos completamente funcionales
- Ejercicio 1: GET requests con GitHub API
- Ejercicio 2: CRUD completo (POST, PUT, PATCH, DELETE)
- Ejercicio 3: Manejo robusto de errores y timeouts
- Ejercicio 4: Reintentos con backoff exponencial y jitter
- Ejercicio 5: Cliente reutilizable con httpx.Client
- Ejercicio 6: Streaming de archivos con barra de progreso
- Uso de APIs públicas: GitHub, JSONPlaceholder, HTTPBin
- Type hints completos y 100% PEP 8 compliant
- pyproject.toml con Poetry configurado
- Todos los ejercicios son ejecutables

**Ubicación:** [modulo-http-apis/](modulo-http-apis/)

## Próximos Módulos

Los siguientes módulos se agregarán a medida que avance el curso:

- Calidad y testing (pytest)

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
