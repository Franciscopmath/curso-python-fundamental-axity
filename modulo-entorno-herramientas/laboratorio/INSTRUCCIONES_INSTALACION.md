# Instrucciones de Instalación - Solución de Problemas

## Problema: SQLite3 no disponible en Python 3.12

Si al ejecutar `poetry run pre-commit install` obtienes un error:
```
ModuleNotFoundError: No module named '_sqlite3'
```

### Solución: Reinstalar Python 3.12 con dependencias del sistema

**Paso 1: Instalar dependencias del sistema**

En Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y \
    libsqlite3-dev \
    libbz2-dev \
    libreadline-dev \
    libssl-dev \
    zlib1g-dev \
    libffi-dev \
    liblzma-dev
```

En Fedora/CentOS/RHEL:
```bash
sudo dnf install -y \
    sqlite-devel \
    bzip2-devel \
    readline-devel \
    openssl-devel \
    zlib-devel \
    libffi-devel \
    xz-devel
```

**Paso 2: Desinstalar y reinstalar Python 3.12**

```bash
# Activar pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

# Desinstalar versión actual
pyenv uninstall 3.12.0

# Reinstalar con las dependencias correctas
pyenv install 3.12.0

# Verificar que sqlite3 funciona
python3.12 -c "import sqlite3; print('SQLite3 funciona correctamente')"
```

**Paso 3: Recrear el ambiente virtual de Poetry**

```bash
cd /home/franciscomath/fundamental-level/modulo-entorno-herramientas/laboratorio

# Eliminar ambiente virtual actual
poetry env remove python3.12

# Recrear ambiente virtual
poetry install

# Ahora pre-commit debería funcionar
poetry run pre-commit install
```

## Alternativa: Usar Python 3.10 del sistema

Si no puedes reinstalar Python 3.12, puedes usar Python 3.10:

```bash
cd /home/franciscomath/fundamental-level/modulo-entorno-herramientas/laboratorio

# Editar pyproject.toml
# Cambiar: requires-python = ">=3.12"
# Por:     requires-python = ">=3.10"

# Recrear proyecto
poetry env use python3.10
poetry install

# Instalar pre-commit
poetry run pre-commit install
```

## Verificación Manual de las Herramientas

Mientras tanto, puedes ejecutar las herramientas manualmente:

### Ejecutar Ruff
```bash
poetry run ruff check .
poetry run ruff check --fix .
```

### Ejecutar Black
```bash
poetry run black .
```

### Ejecutar isort
```bash
poetry run isort .
```

### Ejecutar todo junto
```bash
poetry run ruff check --fix . && poetry run isort . && poetry run black .
```

### Ejecutar pre-commit manualmente (sin instalación en git)
```bash
# Requiere que pre-commit funcione (necesita sqlite3)
poetry run pre-commit run --all-files
```

## Estado Actual del Laboratorio

El laboratorio está **completo y funcional** excepto por la instalación automática de pre-commit hooks.

**Lo que funciona:**
- ✅ Python 3.12 instalado con pyenv
- ✅ Poetry configurado
- ✅ Proyecto inicializado
- ✅ black, isort, ruff instalados y funcionando
- ✅ Código de ejemplo con violaciones
- ✅ Código corregido que pasa todas las validaciones
- ✅ Configuración completa en pyproject.toml
- ✅ Archivo .pre-commit-config.yaml creado

**Requiere solución manual:**
- ⚠️  Instalación de pre-commit hooks (necesita sqlite3)

## Comandos de Verificación

```bash
# Verificar Python
python --version

# Verificar Poetry
poetry --version

# Verificar herramientas
poetry run ruff --version
poetry run black --version
poetry run isort --version

# Ver ambiente virtual
poetry env info

# Listar paquetes instalados
poetry show
```

## Resumen

El laboratorio demuestra exitosamente todos los conceptos del módulo. La limitación de sqlite3 es un problema conocido al compilar Python sin las dependencias del sistema, pero no afecta la funcionalidad principal de las herramientas de calidad de código (black, isort, ruff).
