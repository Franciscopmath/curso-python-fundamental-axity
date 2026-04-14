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

### 1. Configuración de Python 3.12 con pyenv

```bash
# Instalar pyenv
curl https://pyenv.run | bash

# Configurar en shell
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

# Instalar Python 3.12
pyenv install 3.12.0

# Establecer versión local para este proyecto
pyenv local 3.12.0
```

### 2. Inicialización del Proyecto con Poetry

```bash
# Inicializar proyecto
poetry init --no-interaction \
  --name "laboratorio-entorno" \
  --description "Laboratorio del módulo Entorno y Herramientas" \
  --python "^3.12"
```

### 3. Instalación de Herramientas de Calidad

```bash
# Instalar herramientas de desarrollo
poetry add --group dev black isort ruff pre-commit pytest
```

### 4. Configuración de Herramientas en pyproject.toml

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

### 5. Configuración de Pre-commit Hooks

El archivo `.pre-commit-config.yaml` configura hooks que se ejecutan automáticamente antes de cada commit:

- trailing-whitespace: Elimina espacios en blanco al final
- end-of-file-fixer: Asegura nueva línea al final
- check-yaml: Valida archivos YAML
- check-added-large-files: Previene commits de archivos grandes
- black: Formateo automático
- isort: Ordenamiento de imports
- ruff: Linting y correcciones automáticas

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

### Instalación de Pre-commit

```bash
# Instalar los hooks de git
poetry run pre-commit install

# Ejecutar manualmente en todos los archivos
poetry run pre-commit run --all-files
```

Una vez instalado, pre-commit se ejecuta automáticamente en cada `git commit`.

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
python --version  # Debe mostrar Python 3.12.0
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

1. **Poetry simplifica la gestión de dependencias** comparado con pip + virtualenv
2. **pyproject.toml centraliza toda la configuración** del proyecto
3. **Black elimina debates sobre estilo** - "The uncompromising formatter"
4. **Ruff es extremadamente rápido** - reemplaza múltiples herramientas
5. **Pre-commit hooks previenen commits con código de mala calidad**
6. **PEP 8 mejora la legibilidad** y consistencia del código
7. **Las herramientas automatizan tareas repetitivas** de formateo

## Próximos Pasos

1. Aplicar estos conocimientos en todos los proyectos Python
2. Configurar el IDE (VS Code/PyCharm) con las mismas herramientas
3. Estudiar los siguientes módulos del curso
4. Practicar escribiendo código que cumpla PEP 8 desde el inicio
5. Explorar configuraciones avanzadas de ruff y black

## Referencias

- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pre-commit Documentation](https://pre-commit.com/)
