# Laboratorio: Funciones y Programación Pythonic

## 📋 Descripción

Este laboratorio implementa utilidades pythonic avanzadas que demuestran:

- ✅ **Decorador de reintentos con backoff exponencial**
- ✅ **Generadores por lotes (batch processing)**
- ✅ **Context managers de temporización**
- ✅ **Closures y programación funcional**
- ✅ **Type hints completos**
- ✅ **100% PEP 8 compliant**

## 🎯 Objetivos del Laboratorio

1. **Diseñar APIs de funciones claras**: Usar *args/**kwargs, type hints
2. **Implementar decoradores útiles**: Retry con backoff exponencial
3. **Crear generadores eficientes**: Batch processing para grandes datasets
4. **Desarrollar context managers**: Gestión de recursos y temporización

## 📁 Estructura del Proyecto

```
laboratorio/
├── pyproject.toml              # Configuración Poetry + herramientas
├── utilidades_pythonic.py      # Implementación completa
└── README.md                   # Este archivo
```

## 🚀 Instalación y Configuración

### 1. Activar el entorno virtual

```bash
cd modulo-funciones-pythonic/laboratorio
poetry shell
```

### 2. Instalar dependencias

```bash
poetry install
```

### 3. Ejecutar el script de demostración

```bash
python utilidades_pythonic.py
```

## 💻 Componentes Implementados

### 1. Decorador de Reintentos (`@retry`)

Decorador que reintenta funciones con backoff exponencial y jitter.

**Características:**
- Backoff exponencial configurable
- Jitter aleatorio para evitar thundering herd
- Captura de excepciones específicas
- Preserva metadata de la función original

**Uso:**

```python
from utilidades_pythonic import retry, ReintentosAgotadosError

@retry(max_intentos=5, backoff_factor=2.0, excepciones=(ValueError, IOError))
def operacion_inestable():
    # Código que puede fallar
    resultado = llamada_api_externa()
    return resultado

try:
    resultado = operacion_inestable()
except ReintentosAgotadosError as e:
    print(f"Falló después de todos los reintentos: {e}")
```

**Parámetros:**
- `max_intentos`: Número máximo de intentos (default: 3)
- `backoff_factor`: Factor de multiplicación para el delay (default: 2.0)
- `excepciones`: Tupla de excepciones a capturar (default: (Exception,))
- `jitter`: Agregar variación aleatoria (default: True)

**Fórmula del backoff:**
```
delay = backoff_factor^(intento - 1)
con jitter: delay *= (0.5 + random())  # 0.5x a 1.5x
```

**Ejemplo de salida:**
```
⚠️  Intento 1/5 falló: ValueError: Error temporal
   Reintentando en 1.23 segundos...
⚠️  Intento 2/5 falló: ValueError: Error temporal
   Reintentando en 2.87 segundos...
✅ Éxito en el intento 3
```

### 2. Generador por Lotes (`batch_generator`)

Divide un iterable en lotes de tamaño fijo para procesamiento eficiente.

**Características:**
- Memoria eficiente (procesa bajo demanda)
- Soporta cualquier iterable
- Manejo correcto del último lote

**Uso:**

```python
from utilidades_pythonic import batch_generator

# Procesar 1 millón de registros en lotes de 1000
datos = range(1_000_000)

for lote in batch_generator(datos, batch_size=1000):
    # Procesar cada lote
    procesar_en_base_datos(lote)
    print(f"Procesados {len(lote)} registros")
```

**Variantes implementadas:**

```python
# 1. batch_generator - Retorna listas
for lote in batch_generator(datos, 100):
    print(type(lote))  # <class 'list'>

# 2. chunked - Retorna tuplas (más rápido)
for chunk in chunked(datos, 100):
    print(type(chunk))  # <class 'tuple'>

# 3. windowed - Ventanas deslizantes
for ventana in windowed(datos, 3):
    print(ventana)  # (0, 1, 2), (1, 2, 3), (2, 3, 4), ...
```

**Ejemplo práctico:**

```python
# Procesar archivo grande línea por línea
with open('datos_masivos.txt') as f:
    for lote_lineas in batch_generator(f, 1000):
        # Procesar 1000 líneas a la vez
        resultados = [procesar_linea(l) for l in lote_lineas]
        guardar_resultados(resultados)
```

### 3. Context Managers de Temporización

Tres implementaciones para medir tiempos de ejecución.

#### a) `Temporizador` (Clase)

```python
from utilidades_pythonic import Temporizador

# Uso básico
with Temporizador("Operación compleja"):
    procesar_datos()
    calcular_resultados()
# ⏱️  Operación compleja: 2.3456 segundos

# Acceder a la duración
with Temporizador("Cálculo", silencioso=True) as t:
    resultado = calcular()

print(f"Duración: {t.duracion:.4f}s")
```

#### b) `temporizador` (Función con @contextmanager)

```python
from utilidades_pythonic import temporizador

with temporizador("Procesamiento") as info:
    procesar_datos()

print(f"Inicio: {info['inicio']}")
print(f"Fin: {info['fin']}")
print(f"Duración: {info['duracion']:.4f}s")
```

#### c) `TemporizadorAcumulativo` (Múltiples mediciones)

```python
from utilidades_pythonic import TemporizadorAcumulativo

timer = TemporizadorAcumulativo("Consultas DB")

for i in range(100):
    with timer:
        ejecutar_consulta(i)

# Reporte automático
print(timer.reporte())
# 📊 Reporte: Consultas DB
#    • Ejecuciones: 100
#    • Tiempo total: 5.2340s
#    • Tiempo promedio: 0.0523s

# Acceso programático
print(f"Total: {timer.total:.2f}s")
print(f"Promedio: {timer.promedio:.4f}s")
print(f"Veces: {timer.veces}")
```

## 🧪 Ejemplos de Uso

### Ejemplo 1: API con Reintentos

```python
import requests
from utilidades_pythonic import retry

@retry(max_intentos=3, backoff_factor=2.0, excepciones=(requests.RequestException,))
def llamar_api(url):
    """Llama a una API con reintentos automáticos."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

# Uso
try:
    datos = llamar_api("https://api.example.com/data")
except ReintentosAgotadosError:
    print("API no disponible")
```

### Ejemplo 2: Procesar CSV en Lotes

```python
import csv
from utilidades_pythonic import batch_generator, Temporizador

def procesar_csv_grande(archivo):
    """Procesa un CSV masivo en lotes."""
    with open(archivo) as f:
        lector = csv.DictReader(f)

        for lote in batch_generator(lector, batch_size=5000):
            with Temporizador(f"Lote de {len(lote)}"):
                # Procesar en base de datos
                db.insert_many(lote)
```

### Ejemplo 3: Benchmark de Funciones

```python
from utilidades_pythonic import TemporizadorAcumulativo

# Comparar dos algoritmos
timer_v1 = TemporizadorAcumulativo("Algoritmo v1")
timer_v2 = TemporizadorAcumulativo("Algoritmo v2")

for dato in test_data:
    with timer_v1:
        resultado1 = algoritmo_v1(dato)

    with timer_v2:
        resultado2 = algoritmo_v2(dato)

print(timer_v1.reporte())
print(timer_v2.reporte())

# Comparar
if timer_v1.promedio < timer_v2.promedio:
    print("✅ v1 es más rápido")
else:
    print("✅ v2 es más rápido")
```

### Ejemplo 4: Ventanas Deslizantes para Moving Average

```python
from utilidades_pythonic import windowed

def moving_average(datos, ventana=3):
    """Calcula media móvil con ventanas deslizantes."""
    for valores in windowed(datos, ventana):
        yield sum(valores) / len(valores)

precios = [10, 12, 13, 15, 14, 16, 18, 20]
medias = list(moving_average(precios, ventana=3))
print(medias)
# [11.67, 13.33, 14.0, 15.0, 16.0, 18.0]
```

## 🔧 Validación del Código

### Verificar con ruff

```bash
poetry run ruff check utilidades_pythonic.py
```

**Salida esperada:**
```
All checks passed!
```

### Formatear con black

```bash
poetry run black utilidades_pythonic.py
```

### Ordenar imports con isort

```bash
poetry run isort utilidades_pythonic.py
```

### Ejecutar todas las validaciones

```bash
poetry run ruff check . && \
poetry run black --check . && \
poetry run isort --check-only .
```

## 📊 Salida del Programa

Al ejecutar `python utilidades_pythonic.py`:

```
================================================================================
                    LABORATORIO: FUNCIONES PYTHONIC
================================================================================

Demostraciones de:
  1. Decorador de reintentos con backoff exponencial
  2. Generadores por lotes
  3. Context managers de temporización
  4. Ventanas deslizantes y chunking

================================================================================
EJEMPLO: Decorador de Reintentos con Backoff
================================================================================

🔄 Intentando operación inestable con retry...

⚠️  Intento 1/5 falló: ValueError: Fallo simulado (probabilidad: 0.6)
   Reintentando en 0.87 segundos...
⚠️  Intento 2/5 falló: ValueError: Fallo simulado (probabilidad: 0.6)
   Reintentando en 2.13 segundos...
✅ Éxito en el intento 3

✅ Operación exitosa

================================================================================
EJEMPLO: Generador por Lotes
================================================================================

📦 Procesando 25 elementos en lotes de 5...

Lote 1:
  Procesando lote de 5 elementos: [0, 1, 2, 3, 4]
  → Suma del lote: 10

Lote 2:
  Procesando lote de 5 elementos: [5, 6, 7, 8, 9]
  → Suma del lote: 35

[... más lotes ...]

✅ Suma total: 300

================================================================================
EJEMPLO: Context Managers de Temporización
================================================================================

1️⃣  Temporizador básico:
   Procesando datos...
⏱️  Operación simple: 0.5001 segundos

2️⃣  Temporizador funcional (@contextmanager):
   Suma calculada: 499999500000
⏱️  Cálculo complejo: 0.0234 segundos

3️⃣  Temporizador acumulativo:
   Consulta 1...
   Consulta 2...
   Consulta 3...

📊 Reporte: Consultas DB
   • Ejecuciones: 3
   • Tiempo total: 0.4523s
   • Tiempo promedio: 0.1508s

[... más ejemplos ...]

================================================================================
✅ Todos los ejemplos completados exitosamente
================================================================================
```

## 🎓 Conceptos Demostrados

### Decoradores
- `@functools.wraps` para preservar metadata
- Decoradores con parámetros (factory pattern)
- Type hints en decoradores
- Manejo de *args/**kwargs

### Generadores
- `yield` para generación lazy
- `yield from` para delegación
- Expresiones generadoras
- Eficiencia en memoria

### Context Managers
- Protocolo `__enter__`/`__exit__`
- `@contextmanager` decorator
- Manejo de excepciones en context managers
- Context managers reutilizables

### Programación Funcional
- Closures con estado
- Funciones de orden superior
- Composición de funciones
- Inmutabilidad y side effects

## 📝 Ejercicios Adicionales

Para practicar más, intenta:

1. **Decorador de caché**: Implementar un decorador LRU cache personalizado
2. **Generador de páginas**: Crear un generador que pagine resultados de API
3. **Context manager de transacciones**: Implementar rollback automático
4. **Decorador de rate limiting**: Limitar llamadas por segundo
5. **Generador infinito con filtros**: Pipeline de transformaciones

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"

Asegúrate de estar en el entorno virtual:
```bash
poetry shell
poetry install
```

### El decorador no preserva la función original

Usa `@functools.wraps` en el wrapper:
```python
@functools.wraps(func)
def wrapper(*args, **kwargs):
    return func(*args, **kwargs)
```

### El generador solo funciona una vez

Los generadores son de un solo uso. Crea una función que retorne el generador:
```python
def crear_generador():
    return (x for x in range(10))

gen1 = crear_generador()
gen2 = crear_generador()  # Nuevo generador
```

## 📚 Recursos

- [Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [Generators](https://wiki.python.org/moin/Generators)
- [Context Managers](https://docs.python.org/3/library/contextlib.html)
- [PEP 343 - with statement](https://www.python.org/dev/peps/pep-0343/)
- [functools - Higher-order functions](https://docs.python.org/3/library/functools.html)

## ✅ Checklist de Completitud

- [x] Decorador de reintentos con backoff exponencial
- [x] Backoff con jitter aleatorio
- [x] Manejo de excepciones específicas
- [x] Generador por lotes (batch_generator)
- [x] Generador con ventanas deslizantes (windowed)
- [x] Chunking con tuplas
- [x] Context manager de temporización (clase)
- [x] Context manager funcional (@contextmanager)
- [x] Temporizador acumulativo
- [x] Type hints completos
- [x] Docstrings detallados
- [x] Ejemplos de uso funcionales
- [x] 100% PEP 8 compliant

---

**¡Laboratorio completado!** 🎉

Este módulo demuestra programación pythonic avanzada con decoradores, generadores y context managers.
