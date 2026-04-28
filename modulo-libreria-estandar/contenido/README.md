# Módulo 6: Librería Estándar y E/S

## Tabla de Contenidos

1. [Introducción a la Librería Estándar](#1-introducción-a-la-librería-estándar)
2. [pathlib - Manejo Moderno de Rutas](#2-pathlib---manejo-moderno-de-rutas)
3. [Manejo de Archivos](#3-manejo-de-archivos)
4. [CSV - Datos Tabulares](#4-csv---datos-tabulares)
5. [JSON - Datos Estructurados](#5-json---datos-estructurados)
6. [YAML - Configuración](#6-yaml---configuración)
7. [datetime - Fechas y Horas](#7-datetime---fechas-y-horas)
8. [logging - Sistema de Logs](#8-logging---sistema-de-logs)
9. [subprocess - Automatización](#9-subprocess---automatización)
10. [Buenas Prácticas](#10-buenas-prácticas)

---

## 1. Introducción a la Librería Estándar

La librería estándar de Python incluye módulos para tareas comunes sin necesidad de instalar paquetes externos.

### ¿Por qué usar la librería estándar?

- **Sin dependencias externas**: Incluido con Python
- **Bien probado**: Código maduro y confiable
- **Documentación completa**: Documentación oficial excelente
- **Multiplataforma**: Funciona en Windows, Linux, macOS
- **Mantenido**: Actualizado con cada versión de Python

---

## 2. pathlib - Manejo Moderno de Rutas

`pathlib` es el módulo moderno para trabajar con rutas de archivos y directorios.

### Conceptos Básicos

```python
from pathlib import Path

# Crear rutas
ruta = Path("data/archivo.txt")
ruta_absoluta = Path("/home/usuario/documentos")

# Directorio actual
directorio_actual = Path.cwd()
print(directorio_actual)  # /home/usuario/proyecto

# Directorio home
home = Path.home()
print(home)  # /home/usuario

# Combinar rutas con el operador /
archivo = Path("data") / "config" / "settings.json"
print(archivo)  # data/config/settings.json
```

### Operaciones con Rutas

```python
from pathlib import Path

ruta = Path("data/ventas/2024/enero.csv")

# Propiedades
print(ruta.name)        # enero.csv
print(ruta.stem)        # enero
print(ruta.suffix)      # .csv
print(ruta.parent)      # data/ventas/2024
print(ruta.parents[0])  # data/ventas/2024
print(ruta.parents[1])  # data/ventas
print(ruta.anchor)      # / (en Unix) o C:\ (en Windows)

# Verificar existencia
if ruta.exists():
    print("El archivo existe")

# Verificar tipo
if ruta.is_file():
    print("Es un archivo")

if ruta.is_dir():
    print("Es un directorio")

# Convertir a ruta absoluta
ruta_abs = ruta.absolute()
ruta_res = ruta.resolve()  # Resuelve enlaces simbólicos también
```

### Crear y Eliminar

```python
from pathlib import Path

# Crear directorios
directorio = Path("data/logs")
directorio.mkdir(parents=True, exist_ok=True)
# parents=True: crea directorios intermedios
# exist_ok=True: no falla si ya existe

# Crear archivo vacío
archivo = Path("data/temp.txt")
archivo.touch()

# Eliminar archivo
archivo.unlink()
archivo.unlink(missing_ok=True)  # No falla si no existe

# Eliminar directorio vacío
directorio.rmdir()
```

### Listar Archivos

```python
from pathlib import Path

directorio = Path("data")

# Listar todos los archivos y directorios
for item in directorio.iterdir():
    print(item)

# Buscar con patrón (glob)
for archivo_csv in directorio.glob("*.csv"):
    print(archivo_csv)

# Buscar recursivamente
for archivo_py in directorio.rglob("*.py"):
    print(archivo_py)

# Filtrar solo archivos
archivos = [f for f in directorio.iterdir() if f.is_file()]

# Filtrar solo directorios
directorios = [d for d in directorio.iterdir() if d.is_dir()]
```

### Leer y Escribir con pathlib

```python
from pathlib import Path

archivo = Path("data/notas.txt")

# Escribir texto
archivo.write_text("Hola Mundo\n")

# Leer texto
contenido = archivo.read_text()
print(contenido)

# Escribir bytes
archivo.write_bytes(b"\x00\x01\x02")

# Leer bytes
datos = archivo.read_bytes()
```

---

## 3. Manejo de Archivos

### Context Managers (with)

**Siempre** usar `with` para abrir archivos:

```python
# ✓ Correcto: cierra automáticamente
with open("archivo.txt", "r") as f:
    contenido = f.read()

# ✗ Incorrecto: debes cerrar manualmente
f = open("archivo.txt", "r")
contenido = f.read()
f.close()  # Fácil de olvidar
```

### Modos de Apertura

```python
# Lectura
with open("archivo.txt", "r") as f:      # Texto, lectura
    contenido = f.read()

with open("archivo.bin", "rb") as f:     # Binario, lectura
    datos = f.read()

# Escritura (sobrescribe)
with open("archivo.txt", "w") as f:      # Texto, escritura
    f.write("Nuevo contenido")

with open("archivo.bin", "wb") as f:     # Binario, escritura
    f.write(b"\x00\x01")

# Agregar (append)
with open("archivo.txt", "a") as f:      # Texto, agregar
    f.write("Nueva línea\n")

# Lectura y escritura
with open("archivo.txt", "r+") as f:     # Texto, lectura y escritura
    contenido = f.read()
    f.write("Más texto")
```

### Leer Archivos

```python
# Leer todo el archivo
with open("archivo.txt", "r") as f:
    contenido = f.read()

# Leer línea por línea (eficiente para archivos grandes)
with open("archivo.txt", "r") as f:
    for linea in f:
        print(linea.rstrip())  # rstrip() elimina \n

# Leer todas las líneas en una lista
with open("archivo.txt", "r") as f:
    lineas = f.readlines()

# Leer una línea
with open("archivo.txt", "r") as f:
    primera_linea = f.readline()
```

### Escribir Archivos

```python
# Escribir una cadena
with open("archivo.txt", "w") as f:
    f.write("Primera línea\n")
    f.write("Segunda línea\n")

# Escribir múltiples líneas
lineas = ["Línea 1\n", "Línea 2\n", "Línea 3\n"]
with open("archivo.txt", "w") as f:
    f.writelines(lineas)

# Usando print (menos común pero útil)
with open("archivo.txt", "w") as f:
    print("Hola", file=f)
    print("Mundo", file=f)
```

### Encodings

```python
# UTF-8 (siempre especificar explícitamente)
with open("archivo.txt", "r", encoding="utf-8") as f:
    contenido = f.read()

# Latin-1
with open("archivo.txt", "r", encoding="latin-1") as f:
    contenido = f.read()

# Manejo de errores de encoding
with open("archivo.txt", "r", encoding="utf-8", errors="ignore") as f:
    contenido = f.read()

# errors puede ser: 'ignore', 'replace', 'strict' (default)
```

---

## 4. CSV - Datos Tabulares

### Leer CSV

```python
import csv
from pathlib import Path

# Lectura básica
with open("datos.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for fila in reader:
        print(fila)  # Lista de strings

# Con DictReader (más recomendado)
with open("datos.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        print(fila["nombre"])  # Acceso por nombre de columna
        print(fila["edad"])

# Especificar delimitador
with open("datos.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    for fila in reader:
        print(fila)
```

### Escribir CSV

```python
import csv

# Escritura básica
datos = [
    ["nombre", "edad", "ciudad"],
    ["Ana", 25, "Madrid"],
    ["Juan", 30, "Barcelona"],
]

with open("salida.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(datos)

# Con DictWriter (más recomendado)
datos_dict = [
    {"nombre": "Ana", "edad": 25, "ciudad": "Madrid"},
    {"nombre": "Juan", "edad": 30, "ciudad": "Barcelona"},
]

with open("salida.csv", "w", newline="", encoding="utf-8") as f:
    campos = ["nombre", "edad", "ciudad"]
    writer = csv.DictWriter(f, fieldnames=campos)

    writer.writeheader()  # Escribir encabezados
    writer.writerows(datos_dict)

# Especificar delimitador
with open("salida.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerows(datos)
```

### Manejo Avanzado de CSV

```python
import csv

# Diferentes dialectos
with open("datos.csv", "r") as f:
    reader = csv.reader(f, dialect="excel")  # Excel
    # También: 'excel-tab', 'unix'

# Configuración personalizada
with open("datos.csv", "r") as f:
    reader = csv.reader(
        f,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL,
        skipinitialspace=True
    )
    for fila in reader:
        print(fila)

# Saltar encabezados
with open("datos.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Saltar primera línea
    for fila in reader:
        print(fila)
```

---

## 5. JSON - Datos Estructurados

### Leer JSON

```python
import json
from pathlib import Path

# Desde archivo
with open("datos.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

print(datos["nombre"])
print(datos["edad"])

# Desde string
json_str = '{"nombre": "Ana", "edad": 25}'
datos = json.loads(json_str)
```

### Escribir JSON

```python
import json

datos = {
    "nombre": "Ana",
    "edad": 25,
    "ciudad": "Madrid",
    "activo": True,
    "hobbies": ["leer", "música"],
}

# A archivo
with open("salida.json", "w", encoding="utf-8") as f:
    json.dump(datos, f, indent=2, ensure_ascii=False)
    # indent=2: formato legible
    # ensure_ascii=False: preserva caracteres Unicode

# A string
json_str = json.dumps(datos, indent=2, ensure_ascii=False)
print(json_str)
```

### Opciones de Serialización

```python
import json
from datetime import datetime
from decimal import Decimal

# Custom encoder para tipos no soportados
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

datos = {
    "fecha": datetime.now(),
    "precio": Decimal("19.99"),
}

json_str = json.dumps(datos, cls=CustomEncoder, indent=2)

# Ordenar claves
json_str = json.dumps(datos, sort_keys=True, indent=2)

# Compacto (sin espacios)
json_str = json.dumps(datos, separators=(",", ":"))
```

### Validación y Manejo de Errores

```python
import json

# Manejo de errores
try:
    with open("datos.json", "r") as f:
        datos = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error en JSON: {e}")
    print(f"Línea {e.lineno}, columna {e.colno}")
except FileNotFoundError:
    print("Archivo no encontrado")

# Validar estructura
datos = json.loads(json_str)
if "nombre" in datos and "edad" in datos:
    print("JSON válido")
```

---

## 6. YAML - Configuración

YAML requiere instalación externa: `pip install pyyaml`

### Leer YAML

```python
import yaml
from pathlib import Path

# Desde archivo
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

print(config["database"]["host"])
print(config["database"]["port"])

# Desde string
yaml_str = """
database:
  host: localhost
  port: 5432
app:
  name: MiApp
  debug: true
"""
config = yaml.safe_load(yaml_str)
```

### Escribir YAML

```python
import yaml

config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "user": "admin",
    },
    "app": {
        "name": "MiApp",
        "debug": True,
        "features": ["auth", "api", "logging"],
    },
}

# A archivo
with open("config.yaml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

# A string
yaml_str = yaml.dump(config, default_flow_style=False, allow_unicode=True)
print(yaml_str)
```

### Ejemplo de YAML

```yaml
# config.yaml
database:
  host: localhost
  port: 5432
  credentials:
    user: admin
    password: secret

app:
  name: MiAplicacion
  version: 1.0.0
  debug: false
  features:
    - authentication
    - api
    - logging

servers:
  - name: prod
    ip: 192.168.1.10
  - name: dev
    ip: 192.168.1.20
```

---

## 7. datetime - Fechas y Horas

### Crear Fechas y Horas

```python
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo

# Fecha actual
ahora = datetime.now()
print(ahora)  # 2026-04-28 10:30:45.123456

# Solo fecha
hoy = date.today()
print(hoy)  # 2026-04-28

# Crear fecha específica
fecha = date(2024, 12, 25)
print(fecha)  # 2024-12-25

# Crear datetime específico
dt = datetime(2024, 12, 25, 14, 30, 0)
print(dt)  # 2024-12-25 14:30:00

# Solo hora
hora = time(14, 30, 0)
print(hora)  # 14:30:00
```

### Formatear Fechas

```python
from datetime import datetime

ahora = datetime.now()

# strftime - datetime a string
fecha_str = ahora.strftime("%Y-%m-%d %H:%M:%S")
print(fecha_str)  # 2026-04-28 10:30:45

# Formatos comunes
print(ahora.strftime("%d/%m/%Y"))           # 28/04/2026
print(ahora.strftime("%Y-%m-%d"))           # 2026-04-28
print(ahora.strftime("%H:%M:%S"))           # 10:30:45
print(ahora.strftime("%B %d, %Y"))          # April 28, 2026
print(ahora.strftime("%A, %d de %B"))       # Monday, 28 de April

# ISO format
print(ahora.isoformat())  # 2026-04-28T10:30:45.123456

# strptime - string a datetime
fecha_str = "2024-12-25 14:30:00"
fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
```

### Códigos de Formato

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| %Y | Año (4 dígitos) | 2026 |
| %y | Año (2 dígitos) | 26 |
| %m | Mes (01-12) | 04 |
| %B | Nombre del mes | April |
| %b | Nombre del mes abreviado | Apr |
| %d | Día del mes (01-31) | 28 |
| %A | Nombre del día | Monday |
| %a | Nombre del día abreviado | Mon |
| %H | Hora (00-23) | 10 |
| %I | Hora (01-12) | 10 |
| %M | Minuto (00-59) | 30 |
| %S | Segundo (00-59) | 45 |
| %p | AM/PM | AM |

### Operaciones con Fechas

```python
from datetime import datetime, timedelta

ahora = datetime.now()

# Sumar/restar tiempo
mañana = ahora + timedelta(days=1)
ayer = ahora - timedelta(days=1)
en_una_semana = ahora + timedelta(weeks=1)
hace_dos_horas = ahora - timedelta(hours=2)

# timedelta
delta = timedelta(
    days=7,
    hours=2,
    minutes=30,
    seconds=45
)

fecha_futura = ahora + delta

# Diferencia entre fechas
fecha1 = datetime(2024, 12, 25)
fecha2 = datetime(2024, 12, 31)
diferencia = fecha2 - fecha1

print(diferencia.days)           # 6
print(diferencia.total_seconds()) # 518400.0
```

### Zonas Horarias

```python
from datetime import datetime
from zoneinfo import ZoneInfo

# Hora actual en zona horaria específica
ahora_mexico = datetime.now(ZoneInfo("America/Mexico_City"))
ahora_madrid = datetime.now(ZoneInfo("Europe/Madrid"))
ahora_tokyo = datetime.now(ZoneInfo("Asia/Tokyo"))

print(ahora_mexico)  # 2026-04-28 04:30:45.123456-06:00
print(ahora_madrid)  # 2026-04-28 12:30:45.123456+02:00

# Crear datetime con zona horaria
dt_mexico = datetime(
    2024, 12, 25, 14, 30, 0,
    tzinfo=ZoneInfo("America/Mexico_City")
)

# Convertir entre zonas horarias
dt_madrid = dt_mexico.astimezone(ZoneInfo("Europe/Madrid"))

# UTC
utc_ahora = datetime.now(ZoneInfo("UTC"))
```

---

## 8. logging - Sistema de Logs

### Configuración Básica

```python
import logging

# Configuración simple
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Usar el logger
logging.debug("Mensaje de debug")
logging.info("Mensaje informativo")
logging.warning("Mensaje de advertencia")
logging.error("Mensaje de error")
logging.critical("Mensaje crítico")
```

### Niveles de Log

| Nivel | Valor Numérico | Uso |
|-------|----------------|-----|
| DEBUG | 10 | Información detallada para diagnóstico |
| INFO | 20 | Confirmación de que todo funciona |
| WARNING | 30 | Algo inesperado, pero la app continúa |
| ERROR | 40 | Error que impide una función |
| CRITICAL | 50 | Error grave, la app puede detenerse |

### Logger Personalizado

```python
import logging

# Crear logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Handler para archivo
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)

# Formato
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Agregar handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Usar
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Formatos de Log

```python
import logging

# Formato detallado
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - "
    "%(filename)s:%(lineno)d - %(message)s"
)

# Formato simple
formatter = logging.Formatter("%(levelname)s: %(message)s")

# Formato JSON (para logs estructurados)
formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", '
    '"message": "%(message)s"}'
)
```

### Logging Avanzado

```python
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# Rotación por tamaño
handler = RotatingFileHandler(
    "app.log",
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5            # Mantener 5 archivos
)

# Rotación por tiempo
handler = TimedRotatingFileHandler(
    "app.log",
    when="midnight",  # Rotar a medianoche
    interval=1,       # Cada día
    backupCount=7     # Mantener 7 días
)

# Logging con contexto
logger.info("Usuario %s inició sesión", username)
logger.error("Error al procesar archivo %s: %s", filename, error)

# Logging de excepciones
try:
    resultado = 10 / 0
except ZeroDivisionError:
    logger.exception("Error en división")  # Incluye traceback
```

### Configuración desde Archivo

```python
import logging.config
import yaml

# config_logging.yaml
"""
version: 1
disable_existing_loggers: false

formatters:
  simple:
    format: '%(levelname)s: %(message)s'
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple
    stream: ext://sys.stdout

  file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: detailed
    filename: app.log
    maxBytes: 10485760
    backupCount: 3

loggers:
  myapp:
    level: DEBUG
    handlers: [console, file]
    propagate: false

root:
  level: INFO
  handlers: [console]
"""

# Cargar configuración
with open("config_logging.yaml") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger("myapp")
logger.info("Aplicación iniciada")
```

---

## 9. subprocess - Automatización

### Ejecutar Comandos

```python
import subprocess

# Forma moderna (Python 3.5+)
resultado = subprocess.run(
    ["ls", "-la"],
    capture_output=True,
    text=True,
    check=True
)

print(resultado.stdout)
print(resultado.stderr)
print(resultado.returncode)

# Con shell (usar con precaución)
resultado = subprocess.run(
    "ls -la | grep .py",
    shell=True,
    capture_output=True,
    text=True
)
```

### Opciones de subprocess.run

```python
import subprocess

# Capturar salida
resultado = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True
)

# Verificar código de salida
resultado = subprocess.run(
    ["false"],
    check=True  # Lanza CalledProcessError si falla
)

# Timeout
resultado = subprocess.run(
    ["sleep", "10"],
    timeout=5  # Falla después de 5 segundos
)

# Entrada (stdin)
resultado = subprocess.run(
    ["grep", "error"],
    input="line 1\nerror: something\nline 3\n",
    capture_output=True,
    text=True
)

# Directorio de trabajo
resultado = subprocess.run(
    ["pwd"],
    cwd="/tmp",
    capture_output=True,
    text=True
)

# Variables de entorno
resultado = subprocess.run(
    ["printenv", "MY_VAR"],
    env={"MY_VAR": "valor"},
    capture_output=True,
    text=True
)
```

### Ejemplos Prácticos

```python
import subprocess
from pathlib import Path

# Ejecutar script Python
resultado = subprocess.run(
    ["python", "script.py", "--input", "data.csv"],
    capture_output=True,
    text=True,
    check=True
)

# Git commands
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Update"], check=True)
subprocess.run(["git", "push"], check=True)

# Comprimir archivos
subprocess.run(
    ["tar", "-czf", "backup.tar.gz", "data/"],
    check=True
)

# Buscar archivos
resultado = subprocess.run(
    ["find", ".", "-name", "*.py"],
    capture_output=True,
    text=True
)
archivos = resultado.stdout.strip().split("\n")
```

### Manejo de Errores

```python
import subprocess

try:
    resultado = subprocess.run(
        ["comando_inexistente"],
        capture_output=True,
        text=True,
        check=True
    )
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    print(f"Código de salida: {e.returncode}")
    print(f"Salida: {e.output}")
    print(f"Error: {e.stderr}")
except FileNotFoundError:
    print("Comando no encontrado")
except subprocess.TimeoutExpired:
    print("Comando excedió el tiempo")
```

---

## 10. Buenas Prácticas

### Manejo de Archivos

1. **Siempre usar context managers** (`with`)
2. **Especificar encoding explícitamente** (`encoding="utf-8"`)
3. **Usar pathlib** en lugar de strings para rutas
4. **Validar existencia de archivos** antes de leer
5. **Manejar errores** apropiadamente

```python
from pathlib import Path

# ✓ Buena práctica
archivo = Path("data/config.json")
if archivo.exists():
    with archivo.open("r", encoding="utf-8") as f:
        datos = json.load(f)
else:
    print("Archivo no encontrado")

# ✗ Mala práctica
f = open("data/config.json", "r")
datos = json.load(f)
f.close()
```

### Logging

1. **Usar niveles apropiados**
2. **No usar print() en producción**
3. **Incluir contexto** en mensajes
4. **Configurar rotación** de logs
5. **Logs estructurados** para análisis

```python
import logging

logger = logging.getLogger(__name__)

# ✓ Buena práctica
logger.info("Usuario %s realizó acción %s", user_id, action)
logger.error("Error al procesar archivo %s: %s", filename, error)

# ✗ Mala práctica
print("Error:", error)
logger.info("Error: " + str(error))  # Concatenación costosa
```

### Datos (CSV/JSON)

1. **Validar estructura** de datos
2. **Manejar errores de parseo**
3. **Usar DictReader/DictWriter** para CSV
4. **ensure_ascii=False** para JSON con Unicode
5. **Cerrar archivos** automáticamente con `with`

```python
import csv
import json

# ✓ Buena práctica
with open("datos.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        process(fila)

# Validación JSON
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    if "required_field" not in config:
        raise ValueError("Missing required field")
except json.JSONDecodeError as e:
    logger.error("Invalid JSON: %s", e)
```

### Subprocess

1. **Evitar shell=True** cuando sea posible
2. **Usar lista de argumentos** en lugar de string
3. **Validar entrada** de usuario
4. **Usar timeout** para comandos largos
5. **Capturar y loggear** errores

```python
import subprocess

# ✓ Buena práctica
try:
    resultado = subprocess.run(
        ["comando", "arg1", "arg2"],
        capture_output=True,
        text=True,
        check=True,
        timeout=30
    )
except subprocess.CalledProcessError as e:
    logger.error("Comando falló: %s", e)

# ✗ Mala práctica (inyección de comandos)
user_input = "file.txt; rm -rf /"
subprocess.run(f"cat {user_input}", shell=True)
```

---

## Resumen

- **pathlib**: Manejo moderno de rutas y archivos
- **CSV**: Datos tabulares con csv.DictReader/DictWriter
- **JSON**: Datos estructurados con json.load/dump
- **YAML**: Configuración legible (requiere pyyaml)
- **datetime**: Fechas, horas y zonas horarias
- **logging**: Sistema robusto de logs con niveles
- **subprocess**: Ejecutar comandos externos de forma segura

La librería estándar de Python proporciona herramientas poderosas para E/S, manejo de datos y automatización sin dependencias externas.
