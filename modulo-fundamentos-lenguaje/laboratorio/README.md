# Laboratorio: Fundamentos del Lenguaje Python

## 📋 Descripción

Este laboratorio implementa un sistema de procesamiento de productos almacenados en formato JSON, demostrando los fundamentos del lenguaje Python:

- ✅ Sintaxis e indentación
- ✅ Variables y alcance (local, enclosing, global)
- ✅ Tipos básicos (int, float, str, bool)
- ✅ Colecciones (list, dict, set, tuple)
- ✅ Control de flujo (if, for, while, comprehensions)
- ✅ Manejo robusto de excepciones
- ✅ Argumentos de línea de comandos
- ✅ Expresiones regulares (en validaciones)

## 🎯 Objetivos del Laboratorio

1. **Manejo de estructuras de datos**: Trabajar con listas, diccionarios, sets y tuplas
2. **Control de flujo**: Implementar filtrado, iteración y agregación de datos
3. **Manejo robusto de errores**: Gestionar errores de archivo y formato JSON
4. **Aplicar PEP 8**: Código limpio y bien documentado

## 📁 Estructura del Proyecto

```
laboratorio/
├── pyproject.toml              # Configuración Poetry + herramientas
├── productos.json              # Datos de ejemplo (12 productos)
├── procesador_productos.py     # Script principal
└── README.md                   # Este archivo
```

## 🚀 Instalación y Configuración

### 1. Activar el entorno virtual

```bash
cd modulo-fundamentos-lenguaje/laboratorio
poetry shell
```

### 2. Instalar dependencias (ya instaladas)

```bash
poetry install
```

### 3. Verificar instalación

```bash
python --version  # Debe ser 3.12+
poetry --version
```

## 💻 Uso del Script

### Sintaxis Básica

```bash
python procesador_productos.py <archivo.json> [opciones]
```

### Ejemplos de Uso

#### 1. Mostrar todos los productos

```bash
python procesador_productos.py productos.json
```

**Salida esperada:**
```
✅ Archivo cargado exitosamente: 12 productos

==================================================================================================
📦 REPORTE DE PRODUCTOS (12 productos)
==================================================================================================

1. Laptop Dell XPS 13
   ID: 1
   Categoría: Electrónica
   Precio: $1299.99
   Stock: 15 unidades
   Disponible: ✅ Sí
   Etiquetas: portátil, trabajo, premium

[... más productos ...]

📊 ESTADÍSTICAS:
   Total de productos: 12
   Precio promedio: $430.82
   Rango de precios: $45.99 - $1495.00
   Stock total: 193 unidades
   Valor del inventario: $19376.21
==================================================================================================
```

#### 2. Filtrar por categoría

```bash
python procesador_productos.py productos.json --categoria Electrónica
```

**Salida:**
```
✅ Archivo cargado exitosamente: 12 productos
🔍 Filtrados por categoría 'Electrónica': 3 productos
```

#### 3. Filtrar por rango de precio

```bash
python procesador_productos.py productos.json --precio-min 100 --precio-max 500
```

**Salida:**
```
✅ Archivo cargado exitosamente: 12 productos
🔍 Filtrados por precio: 6 productos
```

#### 4. Solo productos disponibles

```bash
python procesador_productos.py productos.json --disponibles
```

**Salida:**
```
✅ Archivo cargado exitosamente: 12 productos
🔍 Disponibles: 10 productos
```

#### 5. Buscar por etiqueta

```bash
python procesador_productos.py productos.json --etiqueta gaming
```

**Salida:**
```
✅ Archivo cargado exitosamente: 12 productos
🏷️  Con etiqueta 'gaming': 2 productos
```

#### 6. Agrupar por categoría

```bash
python procesador_productos.py productos.json --agrupar
```

**Salida:**
```
✅ Archivo cargado exitosamente: 12 productos

📊 Productos agrupados por categoría:

Accesorios (4 productos):
  - Mouse Logitech MX Master 3 ($99.99)
  - Teclado Mecánico Keychron K2 ($89.99)
  - Webcam Logitech C920 ($79.99)
  - Hub USB-C Anker 7-en-1 ($49.99)

Audio (2 productos):
  - Auriculares Sony WH-1000XM5 ($399.99)
  - Micrófono Blue Yeti ($129.99)

[... más categorías ...]
```

#### 7. Mostrar solo estadísticas

```bash
python procesador_productos.py productos.json --estadisticas
```

**Salida:**
```
✅ Archivo cargado exitosamente: 12 productos

============================================================
📊 ESTADÍSTICAS
============================================================
Total de productos: 12
Precio promedio: $430.82
Precio mínimo: $45.99
Precio máximo: $1495.00
Stock total: 193 unidades
Valor del inventario: $19376.21
============================================================
```

#### 8. Combinar múltiples filtros

```bash
python procesador_productos.py productos.json --categoria Audio --disponibles --precio-max 200
```

**Salida:**
```
✅ Archivo cargado exitosamente: 12 productos
🔍 Filtrados por categoría 'Audio': 2 productos
🔍 Filtrados por precio: 1 productos
🔍 Disponibles: 1 productos
```

### Opciones Disponibles

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `archivo` | Ruta al archivo JSON (requerido) | `productos.json` |
| `-c, --categoria` | Filtrar por categoría | `--categoria Electrónica` |
| `--precio-min` | Precio mínimo | `--precio-min 100` |
| `--precio-max` | Precio máximo | `--precio-max 500` |
| `-d, --disponibles` | Solo productos disponibles | `--disponibles` |
| `-e, --etiqueta` | Buscar por etiqueta | `--etiqueta gaming` |
| `-a, --agrupar` | Agrupar por categoría | `--agrupar` |
| `-s, --estadisticas` | Solo estadísticas | `--estadisticas` |
| `-h, --help` | Mostrar ayuda | `--help` |

## 🔧 Características Implementadas

### 1. Manejo de Excepciones

El script maneja múltiples tipos de errores:

```python
# Archivo no existe
python procesador_productos.py archivo_inexistente.json
# ❌ Error de archivo: El archivo 'archivo_inexistente.json' no existe

# JSON inválido
python procesador_productos.py datos_malos.json
# ❌ Error de formato JSON: JSON inválido en línea 3, columna 5: ...

# Sin permisos
python procesador_productos.py archivo_sin_permisos.json
# ❌ Error de archivo: Sin permisos para leer el archivo
```

### 2. Excepciones Personalizadas

```python
class ErrorArchivoJSON(Exception):
    """Para errores de lectura de archivos"""
    pass

class ErrorFormatoJSON(Exception):
    """Para errores de formato JSON"""
    pass
```

### 3. Estructuras de Datos Utilizadas

- **Listas**: Almacenar y filtrar productos
- **Diccionarios**: Representar productos y estadísticas
- **Sets**: Obtener categorías únicas
- **Tuplas**: Retornar múltiples valores

```python
# Ejemplo de uso de set
def obtener_categorias_unicas(self) -> set:
    categorias = {p.get("categoria", "Sin categoría") for p in self.productos}
    return categorias
```

### 4. Comprehensions

```python
# List comprehension para filtrado
filtrados = [
    p for p in self.productos
    if p.get("categoria", "").lower() == categoria_lower
]

# Dict comprehension para agrupación
agrupados = {
    categoria: [p for p in productos if p.get("categoria") == categoria]
    for categoria in categorias_unicas
}

# Set comprehension para categorías únicas
categorias = {p.get("categoria", "Sin categoría") for p in self.productos}
```

### 5. Type Hints

Todo el código usa anotaciones de tipos:

```python
def calcular_estadisticas(
    self,
    productos: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Calcula estadísticas con tipos explícitos"""
    pass
```

## 📊 Datos de Ejemplo

El archivo [productos.json](productos.json) contiene 12 productos de ejemplo con las siguientes categorías:

- **Electrónica** (3 productos): Laptops, monitores, tablets
- **Accesorios** (4 productos): Mouse, teclados, webcams, hubs
- **Audio** (2 productos): Auriculares, micrófonos
- **Almacenamiento** (1 producto): SSDs
- **Mobiliario** (2 productos): Sillas, lámparas

Cada producto tiene:
- `id`: Identificador único
- `nombre`: Nombre del producto
- `categoria`: Categoría
- `precio`: Precio en USD
- `stock`: Unidades disponibles
- `disponible`: Boolean de disponibilidad
- `especificaciones`: Objeto con detalles técnicos
- `etiquetas`: Lista de etiquetas

## 🧪 Validación del Código

### Verificar con ruff

```bash
poetry run ruff check procesador_productos.py
```

**Salida esperada:**
```
All checks passed!
```

### Formatear con black

```bash
poetry run black procesador_productos.py
```

### Ordenar imports con isort

```bash
poetry run isort procesador_productos.py
```

### Ejecutar todas las validaciones

```bash
poetry run ruff check . && \
poetry run black --check . && \
poetry run isort --check-only .
```

## 🎓 Conceptos Demostrados

### Control de Flujo

```python
# if-elif-else
if precio_min is not None:
    filtrados = [p for p in filtrados if p.get("precio", 0) >= precio_min]
elif precio_max is not None:
    filtrados = [p for p in filtrados if p.get("precio", 0) <= precio_max]
else:
    filtrados = self.productos.copy()

# for con enumerate
for i, producto in enumerate(productos, 1):
    print(f"{i}. {producto['nombre']}")

# while con condiciones
while contador < max_intentos and not exito:
    # procesamiento
    contador += 1
```

### Manejo de Errores

```python
try:
    with open(archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
except FileNotFoundError:
    raise ErrorArchivoJSON(f"No se encontró: {archivo}")
except json.JSONDecodeError as e:
    raise ErrorFormatoJSON(f"JSON inválido: {e.msg}")
except Exception as e:
    raise ErrorArchivoJSON(f"Error inesperado: {e}")
finally:
    print("Limpieza completada")
```

### Variables y Alcance

```python
# Variable global (nivel de módulo)
PRECIO_MAXIMO_DEFECTO = 1000

class ProcesadorProductos:
    # Variable de instancia
    def __init__(self):
        self.productos = []  # Scope de instancia

    def procesar(self):
        # Variable local
        total = 0

        # Función anidada con nonlocal
        def sumar(valor):
            nonlocal total
            total += valor
```

## 📝 Ejercicios Adicionales

Para practicar más, intenta agregar estas funcionalidades:

1. **Ordenamiento**: Agregar opción `--ordenar-por` (precio, nombre, stock)
2. **Búsqueda por nombre**: Usar expresiones regulares para buscar productos
3. **Exportar resultados**: Guardar filtros en un nuevo archivo JSON
4. **Validación de datos**: Verificar que todos los productos tengan campos requeridos
5. **Cálculos avanzados**: Media, mediana, desviación estándar de precios

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'argparse'"

- `argparse` es parte de la biblioteca estándar de Python 3.12
- Verifica la versión: `python --version`

### Error: "No such file or directory: 'productos.json'"

- Asegúrate de estar en el directorio correcto
- Usa ruta relativa o absoluta: `python procesador_productos.py /ruta/completa/productos.json`

### El script no muestra colores o emojis

- En Windows, usa Windows Terminal o PowerShell 7+
- En Linux/Mac, asegúrate que tu terminal soporte UTF-8

## 📚 Recursos

- [Documentación oficial de Python](https://docs.python.org/3/)
- [PEP 8 - Style Guide](https://pep8.org/)
- [argparse Tutorial](https://docs.python.org/3/howto/argparse.html)
- [JSON en Python](https://docs.python.org/3/library/json.html)
- [Type Hints](https://docs.python.org/3/library/typing.html)

## ✅ Checklist de Completitud

- [x] Script lee archivos JSON
- [x] Manejo de errores de archivo (FileNotFoundError, PermissionError)
- [x] Manejo de errores de formato (JSONDecodeError)
- [x] Excepciones personalizadas
- [x] Filtrado por categoría
- [x] Filtrado por precio (min/max)
- [x] Filtrado por disponibilidad
- [x] Búsqueda por etiquetas
- [x] Agregación de datos (estadísticas)
- [x] Agrupación por categoría
- [x] Argumentos de línea de comandos
- [x] Type hints en todas las funciones
- [x] Docstrings completos
- [x] Código cumple PEP 8
- [x] Sin errores de ruff/black/isort

---

**¡Laboratorio completado!** 🎉

Este laboratorio demuestra todos los fundamentos del lenguaje Python requeridos en el módulo.
