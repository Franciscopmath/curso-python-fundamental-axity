# Laboratorio: Entorno y Herramientas

## Objetivo

Demostrar el uso práctico de:
- Poetry para gestión de dependencias
- Ambiente virtual con Python 3.12
- Herramientas de calidad: black, isort, ruff
- Pre-commit hooks
- Corrección de infracciones PEP 8

## Estructura del Proyecto

```
laboratorio/
├── pyproject.toml           # Configuración de Poetry y herramientas
├── .pre-commit-config.yaml  # Configuración de pre-commit hooks
├── codigo_malo.py           # Código con violaciones PEP 8 (ANTES)
├── codigo_corregido.py      # Código corregido (DESPUÉS)
└── README.md                # Este archivo
```

## Pasos Realizados

### 1. Verificación de Python 3.12

Ubuntu 24.04 ya incluye Python 3.12 por defecto:

```bash
# Verificar versión de Python
python3.12 --version  # Debe mostrar Python 3.12.3 o superior

# Verificar que SQLite funciona
python3.12 -c "import sqlite3; print('SQLite:', sqlite3.sqlite_version)"
```

**Nota:** En versiones anteriores de Ubuntu (22.04 o anteriores) se requería pyenv para instalar Python 3.12. Con Ubuntu 24.04 esto ya no es necesario.

### 2. Instalación de Poetry

```bash
# Instalar Poetry (si no está instalado)
curl -sSL https://install.python-poetry.org | python3 -

# Agregar Poetry al PATH (agregar a ~/.bashrc o ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Verificar instalación
poetry --version  # Debe mostrar Poetry 2.3.4 o superior
```

### 3. Inicialización del Proyecto con Poetry

```bash
# Configurar Poetry para usar Python 3.12 del sistema
poetry env use python3.12

# El proyecto ya está inicializado con pyproject.toml
# Solo necesitas instalar las dependencias
poetry install
```

### 4. Instalación de Herramientas de Calidad

Las herramientas ya están definidas en `pyproject.toml` y se instalan automáticamente con `poetry install`:

- **black** (26.3.1+): Formateador de código
- **isort** (8.0.1+): Ordenador de imports
- **ruff** (0.15.10+): Linter ultra rápido
- **pre-commit** (4.5.1+): Hooks de git
- **pytest** (9.0.3+): Framework de testing

### 5. Configuración de Herramientas en pyproject.toml

Las herramientas se configuraron en `pyproject.toml`:

**Black:**
- Longitud de línea: 88 caracteres
- Target: Python 3.12

**isort:**
- Perfil compatible con Black
- Longitud de línea: 88

**Ruff:**
- Linter ultra rápido
- Reglas activadas: E (pycodestyle), W (warnings), F (pyflakes), I (isort), B (bugbear), C4 (comprehensions)

### 6. Configuración de Pre-commit Hooks

El archivo `.pre-commit-config.yaml` configura hooks que se ejecutan automáticamente antes de cada commit:

- **trailing-whitespace**: Elimina espacios en blanco al final
- **end-of-file-fixer**: Asegura nueva línea al final
- **check-yaml**: Valida archivos YAML
- **check-added-large-files**: Previene commits de archivos grandes
- **check-merge-conflict**: Detecta marcadores de conflictos de merge
- **check-toml**: Valida archivos TOML
- **black**: Formateo automático
- **isort**: Ordenamiento de imports
- **ruff**: Linting y correcciones automáticas (con `--fix`)
- **ruff-format**: Formateo adicional con ruff

**Instalación de pre-commit:**

```bash
# Instalar los hooks de git
poetry run pre-commit install

# Ejecutar manualmente en todos los archivos
poetry run pre-commit run --all-files
```

**¿Cómo funciona pre-commit?**

Cuando intentas hacer un `git commit`:

1. **Errores menores** → Pre-commit los corrige automáticamente (espacios, formateo, imports)
   - Debes revisar los cambios y volver a hacer `git add .` y `git commit`
2. **Errores graves** → Pre-commit BLOQUEA el commit
   - Debes corregir manualmente los errores (sintaxis, líneas muy largas, etc.)
3. **Sin errores** → El commit se realiza exitosamente

**Saltar pre-commit (no recomendado):**

```bash
git commit --no-verify -m "Mensaje"
```

## Demostración de Corrección de Código

### Violaciones en `codigo_malo.py`

1. **Imports desordenados y mal formateados**
2. **Nombres de funciones en camelCase** (debe ser snake_case)
3. **Nombres de variables en camelCase**
4. **Clases con snake_case** (debe ser PascalCase)
5. **Falta de espacios alrededor de operadores**
6. **Líneas demasiado largas** (>79 caracteres)
7. **Espacios en blanco innecesarios**
8. **Múltiples statements en una línea**
9. **Comparaciones innecesarias con True/False**
10. **Variables no utilizadas**
11. **Imports no utilizados**
12. **Demasiadas líneas en blanco**

### Uso de las Herramientas

#### Ejecutar Ruff (detectar problemas)

```bash
poetry run ruff check codigo_malo.py
```

Salida esperada:
- Errores de sintaxis según PEP 8
- Variables no utilizadas
- Imports no utilizados
- Comparaciones incorrectas

#### Ejecutar Ruff con autofix

```bash
poetry run ruff check --fix codigo_malo.py
```

Corrige automáticamente:
- Imports no utilizados
- Espacios en blanco
- Algunas violaciones simples

#### Ejecutar isort (ordenar imports)

```bash
poetry run isort codigo_malo.py
```

Reorganiza imports en el orden correcto:
1. Librería estándar
2. Dependencias externas
3. Imports locales

#### Ejecutar Black (formatear código)

```bash
poetry run black codigo_malo.py
```

Aplica formateo consistente:
- Espacios correctos
- Longitud de línea
- Indentación consistente

#### Ejecutar todas las herramientas juntas

```bash
poetry run ruff check --fix . && poetry run isort . && poetry run black .
```


## Resultado: Código Corregido

El archivo `codigo_corregido.py` muestra el código después de aplicar todas las correcciones:

### Principales Cambios

1. **Imports ordenados** según PEP 8
2. **Funciones en snake_case**: `calcular_total()`
3. **Variables en snake_case**: `nombre_usuario`, `apellido_usuario`
4. **Clases en PascalCase**: `UsuarioManager`
5. **Espacios correctos** alrededor de operadores
6. **Líneas dentro del límite** (<88 caracteres)
7. **Comparaciones simplificadas**: `if activo:` en vez de `if activo == True:`
8. **Funciones normales** en vez de lambdas innecesarias
9. **Sin variables/imports** no utilizados
10. **Espaciado consistente**

## Verificación del Ambiente Virtual

```bash
# Ver ubicación del ambiente virtual
poetry env info

# Activar el ambiente
poetry shell

# Ver paquetes instalados
poetry show

# Verificar versión de Python
python --version  # Debe mostrar Python 3.12.3

# Verificar que SQLite funciona
python -c "import sqlite3; print('SQLite:', sqlite3.sqlite_version)"
```

## Comandos Útiles

```bash
# Instalar todas las dependencias
poetry install

# Agregar nueva dependencia de producción
poetry add nombre-paquete

# Agregar dependencia de desarrollo
poetry add --group dev nombre-paquete

# Actualizar dependencias
poetry update

# Ejecutar script en el ambiente
poetry run python mi_script.py

# Activar ambiente virtual
poetry shell

# Ejecutar tests
poetry run pytest

# Ver ayuda de ruff
poetry run ruff --help

# Ver ayuda de black
poetry run black --help
```

## Lecciones Aprendidas

1. **Ubuntu 24.04 incluye Python 3.12** - No se requiere pyenv para versiones modernas
2. **Poetry simplifica la gestión de dependencias** comparado con pip + virtualenv
3. **pyproject.toml centraliza toda la configuración** del proyecto
4. **Black elimina debates sobre estilo** - "The uncompromising formatter"
5. **Ruff es extremadamente rápido** - reemplaza múltiples herramientas
6. **Pre-commit hooks previenen commits con código de mala calidad**
   - Corrigen automáticamente errores menores
   - Bloquean commits con errores graves que requieren corrección manual
7. **PEP 8 mejora la legibilidad** y consistencia del código
8. **Las herramientas automatizan tareas repetitivas** de formateo

## Próximos Pasos

1. Aplicar estos conocimientos en todos los proyectos Python
2. Configurar el IDE (VS Code/PyCharm) con las mismas herramientas
3. Estudiar los siguientes módulos del curso
4. Practicar escribiendo código que cumpla PEP 8 desde el inicio
5. Explorar configuraciones avanzadas de ruff y black

## Notas de Actualización (Ubuntu 24.04)

Este laboratorio fue actualizado de Ubuntu 22.04 a Ubuntu 24.04:

- ✅ **Eliminada dependencia de pyenv** - Ubuntu 24.04 incluye Python 3.12.3
- ✅ **Poetry reinstalado** - Versión 2.3.4 con configuración limpia
- ✅ **SQLite funcional** - Python 3.12 del sistema incluye soporte SQLite
- ✅ **Pre-commit configurado** - Hooks instalados y funcionando
- ✅ **Documentación actualizada** - Instrucciones para Ubuntu 24.04

## Referencias

- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pre-commit Documentation](https://pre-commit.com/)
