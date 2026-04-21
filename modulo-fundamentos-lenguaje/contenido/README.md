# Módulo 2: Fundamentos del Lenguaje Python

## Índice

1. [Sintaxis e Indentación](#1-sintaxis-e-indentación)
2. [Variables y Alcance](#2-variables-y-alcance)
3. [Tipos Básicos](#3-tipos-básicos)
4. [Colecciones](#4-colecciones)
5. [Control de Flujo](#5-control-de-flujo)
6. [Errores y Excepciones](#6-errores-y-excepciones)
7. [Expresiones Regulares](#7-expresiones-regulares)
8. [Mejores Prácticas](#8-mejores-prácticas)

---

## 1. Sintaxis e Indentación

### 1.1 Principios Básicos

Python utiliza **indentación** para definir bloques de código, a diferencia de otros lenguajes que usan llaves `{}` o palabras clave como `end`.

#### Reglas de Indentación:
- **4 espacios** por nivel de indentación (PEP 8)
- No mezclar tabs y espacios
- La consistencia es obligatoria dentro de un bloque

**Ejemplo correcto:**
```python
def saludar(nombre):
    if nombre:
        mensaje = f"Hola, {nombre}"
        print(mensaje)
    else:
        print("Hola, desconocido")
```

**Ejemplo incorrecto:**
```python
def saludar(nombre):
  if nombre:  # 2 espacios
      mensaje = f"Hola, {nombre}"  # 4 espacios
    print(mensaje)  # 2 espacios - ERROR!
```

### 1.2 Comentarios

```python
# Comentario de una línea

"""
Comentario de múltiples líneas
o docstring para documentación
"""

def calcular_total(precio, cantidad):
    """
    Calcula el total de una compra.

    Args:
        precio (float): Precio unitario
        cantidad (int): Cantidad de productos

    Returns:
        float: Total de la compra
    """
    return precio * cantidad
```

### 1.3 Convenciones de Nomenclatura (PEP 8)

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Variables | snake_case | `nombre_usuario` |
| Funciones | snake_case | `calcular_total()` |
| Clases | PascalCase | `UsuarioAdmin` |
| Constantes | UPPER_CASE | `MAX_INTENTOS` |
| Módulos | snake_case | `procesador_datos.py` |

---

## 2. Variables y Alcance

### 2.1 Declaración de Variables

Python es **dinámicamente tipado** - no se declara el tipo explícitamente:

```python
# Asignación simple
nombre = "Juan"
edad = 30
altura = 1.75
activo = True

# Asignación múltiple
x, y, z = 1, 2, 3
a = b = c = 0

# Desempaquetado
coordenadas = (10, 20)
x, y = coordenadas
```

### 2.2 Type Hints (Python 3.5+)

Aunque Python no requiere tipos, se pueden usar **anotaciones** para claridad:

```python
from typing import List, Dict, Optional, Union

def procesar_datos(
    nombre: str,
    edad: int,
    emails: List[str],
    config: Optional[Dict[str, str]] = None
) -> bool:
    """Procesa datos del usuario."""
    if config is None:
        config = {}
    return True

# Ejemplo de uso
resultado: bool = procesar_datos("Ana", 25, ["ana@mail.com"])
```

### 2.3 Alcance de Variables (Scope)

Python utiliza la regla **LEGB**:
- **L**ocal: Variables dentro de una función
- **E**nclosing: Variables en funciones anidadas
- **G**lobal: Variables a nivel de módulo
- **B**uilt-in: Funciones integradas de Python

```python
# Scope Global
contador_global = 0

def funcion_externa():
    # Scope Enclosing
    mensaje = "Externo"

    def funcion_interna():
        # Scope Local
        mensaje_local = "Interno"
        print(mensaje)  # Accede al scope Enclosing
        print(mensaje_local)  # Accede al scope Local

    funcion_interna()

# Modificar variables globales
def incrementar():
    global contador_global
    contador_global += 1

# Modificar variables enclosing
def funcion_externa_2():
    contador = 0

    def incrementar_interno():
        nonlocal contador
        contador += 1

    incrementar_interno()
    return contador
```

**Ejemplo completo:**
```python
# Built-in
print(len([1, 2, 3]))  # len está en built-in scope

# Global
MAX_INTENTOS = 3
intentos = 0

def validar_login(password: str) -> bool:
    """Valida contraseña con intentos limitados."""
    global intentos  # Modificar variable global

    # Local
    password_correcto = "secret123"

    if password == password_correcto:
        intentos = 0  # Resetear
        return True
    else:
        intentos += 1
        if intentos >= MAX_INTENTOS:
            print("Cuenta bloqueada")
        return False
```

---

## 3. Tipos Básicos

### 3.1 Números

```python
# Enteros (int)
edad = 30
poblacion = 1_000_000  # Guiones bajos para legibilidad
binario = 0b1010  # 10 en binario
hexadecimal = 0xFF  # 255 en hexadecimal

# Flotantes (float)
precio = 19.99
pi = 3.14159
cientifico = 1.5e-4  # 0.00015

# Complejos (complex)
complejo = 3 + 4j

# Operaciones
suma = 10 + 5
resta = 10 - 5
multiplicacion = 10 * 5
division = 10 / 3  # 3.333... (siempre float)
division_entera = 10 // 3  # 3 (parte entera)
modulo = 10 % 3  # 1 (resto)
potencia = 2 ** 8  # 256

# Funciones útiles
abs(-10)  # 10
round(3.7)  # 4
max(1, 5, 3)  # 5
min(1, 5, 3)  # 1
```

### 3.2 Cadenas (str)

```python
# Declaración
nombre = "Juan"
apellido = 'Pérez'
multilinea = """
Esto es un texto
de múltiples líneas
"""

# Formateo
edad = 30
# f-strings (Python 3.6+) - RECOMENDADO
mensaje = f"Hola {nombre}, tienes {edad} años"
# format()
mensaje = "Hola {}, tienes {} años".format(nombre, edad)
# % (antiguo)
mensaje = "Hola %s, tienes %d años" % (nombre, edad)

# Operaciones
texto = "Python"
texto.upper()  # "PYTHON"
texto.lower()  # "python"
texto.capitalize()  # "Python"
texto.strip()  # Elimina espacios
texto.replace("Py", "Ja")  # "Jathon"
texto.split(",")  # Divide en lista
",".join(["a", "b", "c"])  # "a,b,c"

# Slicing
texto = "Python"
texto[0]  # "P"
texto[-1]  # "n"
texto[0:3]  # "Pyt"
texto[::-1]  # "nohtyP" (invertir)

# Métodos de validación
"123".isdigit()  # True
"abc".isalpha()  # True
"abc123".isalnum()  # True
"   ".isspace()  # True
```

### 3.3 Booleanos (bool)

```python
# Valores
verdadero = True
falso = False

# Operadores lógicos
resultado = True and False  # False
resultado = True or False  # True
resultado = not True  # False

# Valores falsy (se evalúan como False)
bool(0)  # False
bool("")  # False
bool([])  # False
bool({})  # False
bool(None)  # False

# Valores truthy (se evalúan como True)
bool(1)  # True
bool("texto")  # True
bool([1, 2])  # True

# Comparaciones
5 > 3  # True
5 == 5  # True
5 != 3  # True
5 >= 5  # True
"a" in "casa"  # True
"x" not in "casa"  # True

# Comparaciones encadenadas
1 < 5 < 10  # True (equivale a: 1 < 5 and 5 < 10)
```

### 3.4 None

Representa la ausencia de valor:

```python
resultado = None

def funcion_sin_return():
    pass

valor = funcion_sin_return()  # None

# Verificar None
if valor is None:
    print("Sin valor")

# NO usar == para None
if valor == None:  # ❌ Incorrecto
    pass

if valor is None:  # ✅ Correcto
    pass
```

---

## 4. Colecciones

### 4.1 Listas (list)

**Características:**
- Ordenadas
- Mutables (se pueden modificar)
- Permiten duplicados
- Acceso por índice

```python
# Creación
numeros = [1, 2, 3, 4, 5]
mixta = [1, "dos", 3.0, True]
vacia = []
lista = list(range(5))  # [0, 1, 2, 3, 4]

# Acceso
numeros[0]  # 1
numeros[-1]  # 5 (último)
numeros[1:3]  # [2, 3] (slicing)

# Modificación
numeros[0] = 10
numeros.append(6)  # Agregar al final
numeros.insert(0, 0)  # Insertar en posición
numeros.extend([7, 8])  # Agregar múltiples
numeros.remove(3)  # Eliminar por valor
del numeros[0]  # Eliminar por índice
ultimo = numeros.pop()  # Eliminar y devolver último
numeros.clear()  # Vaciar lista

# Operaciones
len(numeros)  # Longitud
3 in numeros  # Verificar existencia
numeros.count(2)  # Contar ocurrencias
numeros.index(5)  # Obtener índice
numeros.sort()  # Ordenar in-place
numeros.reverse()  # Invertir in-place
sorted(numeros)  # Nueva lista ordenada
reversed(numeros)  # Iterador invertido

# List comprehension
cuadrados = [x**2 for x in range(10)]
pares = [x for x in range(10) if x % 2 == 0]
matriz = [[i*j for j in range(3)] for i in range(3)]
```

**Ejemplo práctico:**
```python
# Procesar lista de productos
productos = [
    {"nombre": "Laptop", "precio": 1200},
    {"nombre": "Mouse", "precio": 25},
    {"nombre": "Teclado", "precio": 80}
]

# Filtrar productos caros
caros = [p for p in productos if p["precio"] > 50]

# Obtener solo nombres
nombres = [p["nombre"] for p in productos]

# Calcular total
total = sum(p["precio"] for p in productos)
```

### 4.2 Tuplas (tuple)

**Características:**
- Ordenadas
- **Inmutables** (no se pueden modificar)
- Permiten duplicados
- Más eficientes que listas

```python
# Creación
coordenadas = (10, 20)
colores = ("rojo", "verde", "azul")
unitaria = (5,)  # Coma necesaria para tupla de 1 elemento
vacia = ()

# Acceso (igual que listas)
coordenadas[0]  # 10
coordenadas[-1]  # 20

# Desempaquetado
x, y = coordenadas
r, g, b = colores

# Desempaquetado extendido
primero, *resto = (1, 2, 3, 4, 5)
# primero = 1, resto = [2, 3, 4, 5]

# Operaciones
len(coordenadas)
10 in coordenadas
coordenadas.count(10)
coordenadas.index(20)

# Conversión
lista = list(coordenadas)
tupla = tuple([1, 2, 3])
```

**Cuándo usar tuplas:**
```python
# Datos que no deben cambiar
DIAS_SEMANA = ("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom")

# Retornar múltiples valores
def obtener_coordenadas():
    return (40.7128, -74.0060)  # NYC

# Como claves de diccionario
ubicaciones = {
    (40.7128, -74.0060): "New York",
    (34.0522, -118.2437): "Los Angeles"
}
```

### 4.3 Diccionarios (dict)

**Características:**
- Pares clave-valor
- Desordenados (ordenados desde Python 3.7+ por inserción)
- Mutables
- Claves únicas

```python
# Creación
persona = {
    "nombre": "Juan",
    "edad": 30,
    "ciudad": "Madrid"
}

# Otras formas
persona = dict(nombre="Juan", edad=30)
persona = dict([("nombre", "Juan"), ("edad", 30)])

# Acceso
nombre = persona["nombre"]  # Error si no existe
edad = persona.get("edad")  # None si no existe
edad = persona.get("edad", 0)  # 0 si no existe (valor por defecto)

# Modificación
persona["edad"] = 31  # Actualizar
persona["email"] = "juan@mail.com"  # Agregar
del persona["ciudad"]  # Eliminar
persona.pop("edad")  # Eliminar y devolver
persona.clear()  # Vaciar

# Operaciones
len(persona)
"nombre" in persona  # Verificar clave
persona.keys()  # Vista de claves
persona.values()  # Vista de valores
persona.items()  # Vista de pares (clave, valor)

# Fusionar diccionarios
defaults = {"tema": "claro", "idioma": "es"}
config = {"idioma": "en"}
config_final = {**defaults, **config}  # {'tema': 'claro', 'idioma': 'en'}

# Python 3.9+
config_final = defaults | config

# Actualizar
persona.update({"edad": 32, "telefono": "123456"})

# Dict comprehension
cuadrados = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Diccionarios anidados
usuarios = {
    "admin": {"nombre": "Admin", "permisos": ["read", "write"]},
    "user": {"nombre": "Usuario", "permisos": ["read"]}
}
```

**Ejemplo práctico:**
```python
# Contar palabras
texto = "python es genial python es poderoso"
palabras = texto.split()
conteo = {}
for palabra in palabras:
    conteo[palabra] = conteo.get(palabra, 0) + 1
# {'python': 2, 'es': 2, 'genial': 1, 'poderoso': 1}

# Alternativa con defaultdict
from collections import defaultdict
conteo = defaultdict(int)
for palabra in palabras:
    conteo[palabra] += 1
```

### 4.4 Conjuntos (set)

**Características:**
- Desordenados
- Elementos únicos (sin duplicados)
- Mutables
- Operaciones matemáticas de conjuntos

```python
# Creación
numeros = {1, 2, 3, 4, 5}
vacio = set()  # NO usar {} (es diccionario)
desde_lista = set([1, 2, 2, 3, 3])  # {1, 2, 3}

# Agregar/eliminar
numeros.add(6)
numeros.remove(3)  # Error si no existe
numeros.discard(10)  # No error si no existe
numeros.pop()  # Eliminar y devolver elemento aleatorio
numeros.clear()

# Operaciones de conjuntos
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Unión
a | b  # {1, 2, 3, 4, 5, 6}
a.union(b)

# Intersección
a & b  # {3, 4}
a.intersection(b)

# Diferencia
a - b  # {1, 2}
a.difference(b)

# Diferencia simétrica
a ^ b  # {1, 2, 5, 6}
a.symmetric_difference(b)

# Subconjunto/superconjunto
{1, 2}.issubset({1, 2, 3})  # True
{1, 2, 3}.issuperset({1, 2})  # True

# Set comprehension
pares = {x for x in range(10) if x % 2 == 0}
```

**Ejemplo práctico:**
```python
# Eliminar duplicados
emails = ["a@mail.com", "b@mail.com", "a@mail.com"]
unicos = list(set(emails))

# Encontrar elementos comunes
usuarios_grupo_a = {"Juan", "Ana", "Pedro"}
usuarios_grupo_b = {"Ana", "Luis", "Pedro"}
en_ambos = usuarios_grupo_a & usuarios_grupo_b  # {'Ana', 'Pedro'}
```

### 4.5 Comparación de Colecciones

| Característica | List | Tuple | Dict | Set |
|----------------|------|-------|------|-----|
| Ordenado | ✅ | ✅ | ✅ (3.7+) | ❌ |
| Mutable | ✅ | ❌ | ✅ | ✅ |
| Duplicados | ✅ | ✅ | Claves únicas | ❌ |
| Indexado | ✅ | ✅ | Por clave | ❌ |
| Sintaxis | `[]` | `()` | `{}` | `{}` |
| Uso común | Secuencias | Inmutables | Clave-valor | Únicos |

---

## 5. Control de Flujo

### 5.1 Condicionales (if-elif-else)

```python
# if simple
edad = 18
if edad >= 18:
    print("Mayor de edad")

# if-else
if edad >= 18:
    print("Mayor de edad")
else:
    print("Menor de edad")

# if-elif-else
nota = 85
if nota >= 90:
    print("A")
elif nota >= 80:
    print("B")
elif nota >= 70:
    print("C")
else:
    print("F")

# Operador ternario
mensaje = "Mayor" if edad >= 18 else "Menor"

# Condiciones múltiples
edad = 25
licencia = True
if edad >= 18 and licencia:
    print("Puede conducir")

# Verificar múltiples valores
color = "rojo"
if color in ("rojo", "amarillo", "verde"):
    print("Color válido")
```

### 5.2 Match-Case (Python 3.10+)

Similar a `switch` en otros lenguajes, pero más poderoso:

```python
# Match simple
comando = "start"
match comando:
    case "start":
        print("Iniciando...")
    case "stop":
        print("Deteniendo...")
    case "pause":
        print("Pausando...")
    case _:
        print("Comando desconocido")

# Match con patrones
def procesar_punto(punto):
    match punto:
        case (0, 0):
            print("Origen")
        case (0, y):
            print(f"Eje Y: {y}")
        case (x, 0):
            print(f"Eje X: {x}")
        case (x, y):
            print(f"Punto: ({x}, {y})")
        case _:
            print("No es un punto válido")

# Match con tipos
def procesar_dato(dato):
    match dato:
        case int(n):
            print(f"Entero: {n}")
        case str(s):
            print(f"Cadena: {s}")
        case [x, y]:
            print(f"Lista de 2 elementos: {x}, {y}")
        case {"nombre": nombre, "edad": edad}:
            print(f"{nombre} tiene {edad} años")
        case _:
            print("Tipo desconocido")

# Match con guardas
def clasificar_numero(n):
    match n:
        case n if n < 0:
            print("Negativo")
        case 0:
            print("Cero")
        case n if n > 0 and n < 10:
            print("Positivo de un dígito")
        case _:
            print("Positivo de múltiples dígitos")
```

**Nota:** Para este curso usaremos principalmente `if-elif-else` ya que el laboratorio no requiere pattern matching.

### 5.3 Bucle for

```python
# Iterar sobre lista
frutas = ["manzana", "banana", "naranja"]
for fruta in frutas:
    print(fruta)

# Iterar con índice
for i, fruta in enumerate(frutas):
    print(f"{i}: {fruta}")

# Iterar sobre rango
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):  # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
    print(i)

# Iterar sobre diccionario
persona = {"nombre": "Juan", "edad": 30}

for clave in persona:
    print(clave)  # nombre, edad

for valor in persona.values():
    print(valor)  # Juan, 30

for clave, valor in persona.items():
    print(f"{clave}: {valor}")

# Iterar sobre múltiples listas
nombres = ["Juan", "Ana", "Pedro"]
edades = [30, 25, 35]
for nombre, edad in zip(nombres, edades):
    print(f"{nombre}: {edad} años")

# break y continue
for i in range(10):
    if i == 3:
        continue  # Saltar iteración
    if i == 7:
        break  # Salir del bucle
    print(i)

# else en for (se ejecuta si NO hubo break)
for i in range(5):
    if i == 10:
        break
else:
    print("Bucle completado sin break")
```

### 5.4 Bucle while

```python
# while simple
contador = 0
while contador < 5:
    print(contador)
    contador += 1

# while con condición compleja
intentos = 0
MAX_INTENTOS = 3
exito = False

while intentos < MAX_INTENTOS and not exito:
    password = input("Contraseña: ")
    if password == "secreto":
        exito = True
    else:
        intentos += 1

# while True (bucle infinito controlado)
while True:
    comando = input("Comando (exit para salir): ")
    if comando == "exit":
        break
    print(f"Ejecutando: {comando}")

# else en while
contador = 0
while contador < 3:
    print(contador)
    contador += 1
else:
    print("Bucle terminado normalmente")
```

### 5.5 Comprehensions

```python
# List comprehension
cuadrados = [x**2 for x in range(10)]
pares = [x for x in range(10) if x % 2 == 0]
matriz = [[i*j for j in range(3)] for i in range(3)]

# Dict comprehension
cuadrados_dict = {x: x**2 for x in range(5)}
invertido = {v: k for k, v in {"a": 1, "b": 2}.items()}

# Set comprehension
pares_set = {x for x in range(10) if x % 2 == 0}

# Generator expression (más eficiente en memoria)
suma = sum(x**2 for x in range(1000000))  # No crea lista en memoria
```

---

## 6. Errores y Excepciones

### 6.1 Tipos de Excepciones Comunes

```python
# ZeroDivisionError
resultado = 10 / 0

# ValueError
numero = int("abc")

# TypeError
resultado = "5" + 5

# KeyError
persona = {"nombre": "Juan"}
edad = persona["edad"]

# IndexError
lista = [1, 2, 3]
elemento = lista[10]

# FileNotFoundError
with open("archivo_inexistente.txt") as f:
    contenido = f.read()

# AttributeError
texto = "hola"
texto.push("!")  # str no tiene método push

# NameError
print(variable_no_definida)

# ImportError
from modulo_inexistente import funcion
```

### 6.2 Manejo de Excepciones (try-except)

```python
# try-except básico
try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("No se puede dividir por cero")

# Múltiples excepciones
try:
    numero = int(input("Número: "))
    resultado = 10 / numero
except ValueError:
    print("Entrada inválida")
except ZeroDivisionError:
    print("No se puede dividir por cero")

# Múltiples excepciones en una línea
try:
    # código
    pass
except (ValueError, TypeError):
    print("Error de tipo o valor")

# Capturar el objeto excepción
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
    print(f"Tipo: {type(e)}")

# else (se ejecuta si NO hay excepción)
try:
    resultado = 10 / 2
except ZeroDivisionError:
    print("Error de división")
else:
    print(f"Resultado: {resultado}")

# finally (siempre se ejecuta)
try:
    archivo = open("datos.txt")
    contenido = archivo.read()
except FileNotFoundError:
    print("Archivo no encontrado")
finally:
    if 'archivo' in locals():
        archivo.close()
    print("Limpieza completada")
```

### 6.3 Manejo Robusto de Errores

```python
import json
from typing import Optional, Dict, Any

def leer_json_seguro(ruta: str) -> Optional[Dict[str, Any]]:
    """
    Lee un archivo JSON con manejo robusto de errores.

    Args:
        ruta: Ruta al archivo JSON

    Returns:
        Diccionario con los datos o None si hay error
    """
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{ruta}' no existe")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error: JSON inválido en línea {e.lineno}, columna {e.colno}")
        print(f"   Mensaje: {e.msg}")
        return None
    except PermissionError:
        print(f"❌ Error: Sin permisos para leer '{ruta}'")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
        return None

# Uso
datos = leer_json_seguro("productos.json")
if datos is not None:
    print(f"✅ Datos cargados: {len(datos)} elementos")
```

### 6.4 Lanzar Excepciones

```python
# raise
def dividir(a, b):
    if b == 0:
        raise ValueError("El divisor no puede ser cero")
    return a / b

# Crear excepciones personalizadas
class ProductoNoEncontradoError(Exception):
    """Excepción cuando un producto no existe."""
    pass

class StockInsuficienteError(Exception):
    """Excepción cuando no hay stock suficiente."""
    def __init__(self, producto, solicitado, disponible):
        self.producto = producto
        self.solicitado = solicitado
        self.disponible = disponible
        mensaje = f"Stock insuficiente de '{producto}': solicitado={solicitado}, disponible={disponible}"
        super().__init__(mensaje)

# Uso
def procesar_venta(producto, cantidad):
    stock_disponible = 5
    if cantidad > stock_disponible:
        raise StockInsuficienteError(producto, cantidad, stock_disponible)

try:
    procesar_venta("Laptop", 10)
except StockInsuficienteError as e:
    print(f"Error: {e}")
    print(f"Disponible: {e.disponible}")
```

### 6.5 Context Managers (with)

Manejan automáticamente recursos (archivos, conexiones):

```python
# Sin context manager (manual)
archivo = open("datos.txt")
try:
    contenido = archivo.read()
finally:
    archivo.close()

# Con context manager (automático)
with open("datos.txt") as archivo:
    contenido = archivo.read()
# archivo.close() se llama automáticamente

# Múltiples context managers
with open("entrada.txt") as entrada, open("salida.txt", "w") as salida:
    for linea in entrada:
        salida.write(linea.upper())
```

### 6.6 Mejores Prácticas

```python
# ❌ MAL: Capturar todas las excepciones
try:
    # código
    pass
except:
    pass  # Silencia todos los errores, incluso KeyboardInterrupt

# ✅ BIEN: Capturar excepciones específicas
try:
    datos = json.load(archivo)
except json.JSONDecodeError as e:
    print(f"JSON inválido: {e}")

# ❌ MAL: Excepciones genéricas para control de flujo
try:
    valor = diccionario[clave]
except:
    valor = None

# ✅ BIEN: Usar métodos apropiados
valor = diccionario.get(clave)

# ✅ BIEN: Logging de errores
import logging

try:
    resultado = operacion_critica()
except Exception as e:
    logging.error(f"Error en operación crítica: {e}", exc_info=True)
    raise  # Re-lanzar para que el llamador lo maneje
```

---

## 7. Expresiones Regulares

Las expresiones regulares (regex) permiten buscar y manipular patrones en texto.

### 7.1 Módulo re

```python
import re

# Buscar patrón
texto = "Mi email es juan@example.com"
patron = r'\w+@\w+\.\w+'
match = re.search(patron, texto)
if match:
    print(match.group())  # juan@example.com

# Métodos principales
re.search(patron, texto)    # Encuentra primera ocurrencia
re.match(patron, texto)     # Busca al inicio del texto
re.findall(patron, texto)   # Lista de todas las ocurrencias
re.finditer(patron, texto)  # Iterador de matches
re.sub(patron, repl, texto) # Reemplazar
re.split(patron, texto)     # Dividir
```

### 7.2 Sintaxis de Patrones

```python
# Caracteres literales
r'python'  # Busca "python"

# Metacaracteres
r'.'   # Cualquier carácter (excepto nueva línea)
r'^'   # Inicio de línea
r'$'   # Fin de línea
r'*'   # 0 o más repeticiones
r'+'   # 1 o más repeticiones
r'?'   # 0 o 1 repetición
r'{n}' # Exactamente n repeticiones
r'{n,m}' # Entre n y m repeticiones

# Clases de caracteres
r'[abc]'   # a, b, o c
r'[^abc]'  # Cualquiera excepto a, b, c
r'[a-z]'   # Cualquier minúscula
r'[A-Z]'   # Cualquier mayúscula
r'[0-9]'   # Cualquier dígito

# Secuencias predefinidas
r'\d'  # Dígito [0-9]
r'\D'  # No dígito
r'\w'  # Alfanumérico [a-zA-Z0-9_]
r'\W'  # No alfanumérico
r'\s'  # Espacio en blanco
r'\S'  # No espacio en blanco

# Grupos
r'(abc)'     # Grupo de captura
r'(?:abc)'   # Grupo sin captura
r'(a|b)'     # a o b

# Anclas
r'\b'  # Límite de palabra
r'\B'  # No límite de palabra
```

### 7.3 Ejemplos Prácticos

```python
import re

# Validar email
def validar_email(email: str) -> bool:
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

print(validar_email("usuario@example.com"))  # True
print(validar_email("invalido@"))  # False

# Extraer teléfonos
texto = "Llámame al 555-1234 o al (555) 5678"
telefonos = re.findall(r'\(?\d{3}\)?[-\s]?\d{4}', texto)
print(telefonos)  # ['555-1234', '(555) 5678']

# Reemplazar URLs
texto = "Visita https://example.com y http://test.com"
sin_urls = re.sub(r'https?://[^\s]+', '[URL]', texto)
print(sin_urls)  # Visita [URL] y [URL]

# Extraer datos estructurados
log = "2024-01-15 10:30:45 ERROR Usuario no encontrado"
patron = r'(?P<fecha>\d{4}-\d{2}-\d{2}) (?P<hora>\d{2}:\d{2}:\d{2}) (?P<nivel>\w+) (?P<mensaje>.*)'
match = re.search(patron, log)
if match:
    print(match.group('fecha'))    # 2024-01-15
    print(match.group('nivel'))    # ERROR
    print(match.groupdict())       # Diccionario con todos los grupos

# Validar formato de datos
def validar_codigo_producto(codigo: str) -> bool:
    """Valida formato: 2 letras + 4 dígitos (ej: AB1234)"""
    return bool(re.match(r'^[A-Z]{2}\d{4}$', codigo))

# Limpiar texto
def limpiar_espacios(texto: str) -> str:
    """Elimina espacios múltiples y espacios al inicio/fin."""
    texto = re.sub(r'\s+', ' ', texto)  # Múltiples espacios -> 1
    return texto.strip()

print(limpiar_espacios("  Hola    mundo  "))  # "Hola mundo"

# Buscar palabras completas
texto = "Python es pythonic, no python3"
# Buscar "python" como palabra completa (case-insensitive)
matches = re.findall(r'\bpython\b', texto, re.IGNORECASE)
print(matches)  # ['Python', 'python']
```

### 7.4 Flags (Modificadores)

```python
import re

texto = "Python\nes\ngenial"

# re.IGNORECASE (re.I) - Ignorar mayúsculas/minúsculas
re.findall(r'python', texto, re.IGNORECASE)  # ['Python']

# re.MULTILINE (re.M) - ^ y $ coinciden con inicio/fin de cada línea
re.findall(r'^e', texto, re.MULTILINE)  # ['e']

# re.DOTALL (re.S) - . coincide con nueva línea
re.search(r'Python.*genial', texto, re.DOTALL)  # Match

# Combinar flags
re.findall(r'^python', texto, re.IGNORECASE | re.MULTILINE)
```

---

## 8. Mejores Prácticas

### 8.1 Zen de Python (PEP 20)

```python
import this
```

Principios clave:
1. **Explícito es mejor que implícito**
2. **Simple es mejor que complejo**
3. **Legibilidad cuenta**
4. **Los errores nunca deberían pasar silenciosamente**
5. **Debería haber una - y preferiblemente solo una - manera obvia de hacerlo**

### 8.2 Código Limpio

```python
# ❌ MAL: Nombres poco descriptivos
def f(x, y):
    return x + y

# ✅ BIEN: Nombres descriptivos
def calcular_total(precio, cantidad):
    return precio * cantidad

# ❌ MAL: Magic numbers
if edad > 18:
    pass

# ✅ BIEN: Constantes nombradas
EDAD_MINIMA_ADULTO = 18
if edad > EDAD_MINIMA_ADULTO:
    pass

# ❌ MAL: Funciones largas
def procesar():
    # 100 líneas de código
    pass

# ✅ BIEN: Funciones pequeñas y enfocadas
def validar_entrada():
    pass

def procesar_datos():
    pass

def guardar_resultado():
    pass

# ❌ MAL: Comentarios obvios
i = i + 1  # Incrementar i

# ✅ BIEN: Comentarios que explican el "por qué"
i = i + 1  # Compensar índice base-0 en la API externa
```

### 8.3 Type Hints y Documentación

```python
from typing import List, Dict, Optional

def procesar_productos(
    productos: List[Dict[str, any]],
    filtro: Optional[str] = None
) -> Dict[str, float]:
    """
    Procesa una lista de productos y calcula estadísticas.

    Args:
        productos: Lista de diccionarios con información de productos
        filtro: Categoría opcional para filtrar productos

    Returns:
        Diccionario con estadísticas calculadas (total, promedio, etc.)

    Raises:
        ValueError: Si la lista de productos está vacía

    Example:
        >>> productos = [{"nombre": "Laptop", "precio": 1000}]
        >>> procesar_productos(productos)
        {'total': 1000, 'promedio': 1000}
    """
    if not productos:
        raise ValueError("La lista de productos no puede estar vacía")

    # Implementación...
    return {"total": 0, "promedio": 0}
```

### 8.4 Testing

```python
# tests/test_procesador.py
import pytest
from procesador import calcular_total

def test_calcular_total_positivo():
    assert calcular_total(10, 5) == 50

def test_calcular_total_cero():
    assert calcular_total(0, 5) == 0

def test_calcular_total_negativo():
    with pytest.raises(ValueError):
        calcular_total(-10, 5)
```

---

## Resumen

En este módulo has aprendido:

✅ **Sintaxis e indentación**: Reglas básicas de Python
✅ **Variables y alcance**: LEGB, global, nonlocal
✅ **Tipos básicos**: int, float, str, bool, None
✅ **Colecciones**: list, tuple, dict, set
✅ **Control de flujo**: if, for, while, comprehensions
✅ **Excepciones**: try-except-finally, excepciones personalizadas
✅ **Expresiones regulares**: Buscar y validar patrones
✅ **Mejores prácticas**: Código limpio, documentación, testing

## Recursos Adicionales

- [Documentación oficial de Python](https://docs.python.org/3/)
- [PEP 8 - Guía de estilo](https://pep8.org/)
- [PEP 20 - Zen de Python](https://www.python.org/dev/peps/pep-0020/)
- [Real Python - Tutorials](https://realpython.com/)
- [Python re - Documentación](https://docs.python.org/3/library/re.html)

---

**Próximo paso:** Completar el laboratorio práctico aplicando estos conceptos.
