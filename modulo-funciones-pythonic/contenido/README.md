# Módulo 3: Funciones y Programación "Pythonic"

## Índice

1. [Funciones](#1-funciones)
2. [Argumentos y Parámetros](#2-argumentos-y-parámetros)
3. [Lambdas](#3-lambdas)
4. [Closures](#4-closures)
5. [Decoradores](#5-decoradores)
6. [Iteradores](#6-iteradores)
7. [Generadores](#7-generadores)
8. [Comprensiones](#8-comprensiones)
9. [Context Managers](#9-context-managers)
10. [Programación Pythonic](#10-programación-pythonic)

---

## 1. Funciones

### 1.1 Definición Básica

```python
def saludar(nombre):
    """Saluda a una persona por su nombre."""
    return f"Hola, {nombre}!"

resultado = saludar("Ana")
print(resultado)  # "Hola, Ana!"
```

### 1.2 Funciones con Valores por Defecto

```python
def calcular_precio(precio, descuento=0, impuesto=0.16):
    """
    Calcula el precio final con descuento e impuesto.

    Args:
        precio: Precio base
        descuento: Descuento en porcentaje (default: 0)
        impuesto: Impuesto en porcentaje (default: 0.16)

    Returns:
        Precio final calculado
    """
    precio_con_descuento = precio * (1 - descuento)
    precio_final = precio_con_descuento * (1 + impuesto)
    return precio_final

# Diferentes formas de llamar
calcular_precio(100)  # 116.0
calcular_precio(100, 0.1)  # 104.4
calcular_precio(100, 0.1, 0.21)  # 108.9
```

### 1.3 Retorno de Múltiples Valores

```python
def obtener_estadisticas(numeros):
    """Calcula estadísticas básicas de una lista."""
    return min(numeros), max(numeros), sum(numeros) / len(numeros)

minimo, maximo, promedio = obtener_estadisticas([1, 2, 3, 4, 5])
print(f"Min: {minimo}, Max: {maximo}, Promedio: {promedio}")
```

### 1.4 Funciones como Objetos de Primera Clase

En Python, las funciones son objetos de primera clase:

```python
def cuadrado(x):
    return x ** 2

def cubo(x):
    return x ** 3

# Asignar función a variable
mi_funcion = cuadrado
print(mi_funcion(5))  # 25

# Pasar función como argumento
def aplicar(func, valor):
    return func(valor)

print(aplicar(cuadrado, 5))  # 25
print(aplicar(cubo, 5))  # 125

# Retornar función
def obtener_operacion(tipo):
    if tipo == "cuadrado":
        return cuadrado
    elif tipo == "cubo":
        return cubo

operacion = obtener_operacion("cuadrado")
print(operacion(5))  # 25
```

---

## 2. Argumentos y Parámetros

### 2.1 Argumentos Posicionales

```python
def restar(a, b):
    return a - b

restar(10, 5)  # 5 (10 - 5)
restar(5, 10)  # -5 (5 - 10)
```

### 2.2 Argumentos Nombrados (Keyword Arguments)

```python
def crear_usuario(nombre, edad, ciudad):
    return {"nombre": nombre, "edad": edad, "ciudad": ciudad}

# Argumentos nombrados (orden no importa)
crear_usuario(edad=30, nombre="Juan", ciudad="Madrid")
```

### 2.3 *args - Argumentos Posicionales Variables

Permite pasar un número variable de argumentos posicionales:

```python
def sumar(*numeros):
    """Suma cualquier cantidad de números."""
    return sum(numeros)

print(sumar(1, 2, 3))  # 6
print(sumar(1, 2, 3, 4, 5))  # 15
print(sumar())  # 0

# args es una tupla
def mostrar_args(*args):
    print(f"Tipo: {type(args)}")
    print(f"Valores: {args}")
    for i, arg in enumerate(args):
        print(f"  Argumento {i}: {arg}")

mostrar_args("a", "b", "c")
# Tipo: <class 'tuple'>
# Valores: ('a', 'b', 'c')
```

### 2.4 **kwargs - Argumentos Nombrados Variables

Permite pasar un número variable de argumentos nombrados:

```python
def crear_perfil(**datos):
    """Crea un perfil con datos arbitrarios."""
    for clave, valor in datos.items():
        print(f"{clave}: {valor}")

crear_perfil(nombre="Ana", edad=25, ciudad="Barcelona")
# nombre: Ana
# edad: 25
# ciudad: Barcelona

# kwargs es un diccionario
def mostrar_kwargs(**kwargs):
    print(f"Tipo: {type(kwargs)}")
    print(f"Valores: {kwargs}")

mostrar_kwargs(a=1, b=2, c=3)
# Tipo: <class 'dict'>
# Valores: {'a': 1, 'b': 2, 'c': 3}
```

### 2.5 Combinando Todos los Tipos

El orden debe ser: posicionales, *args, nombrados con default, **kwargs

```python
def funcion_completa(a, b, *args, c=10, d=20, **kwargs):
    """
    Demuestra todos los tipos de argumentos.

    a, b: posicionales requeridos
    *args: posicionales variables
    c, d: nombrados con default
    **kwargs: nombrados variables
    """
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"c={c}, d={d}")
    print(f"kwargs={kwargs}")

funcion_completa(1, 2, 3, 4, c=100, d=200, x=1000, y=2000)
# a=1, b=2
# args=(3, 4)
# c=100, d=200
# kwargs={'x': 1000, 'y': 2000}
```

### 2.6 Desempaquetado de Argumentos

```python
# Desempaquetar lista con *
numeros = [1, 2, 3, 4, 5]
print(*numeros)  # 1 2 3 4 5

def sumar_tres(a, b, c):
    return a + b + c

valores = [10, 20, 30]
resultado = sumar_tres(*valores)  # Equivale a: sumar_tres(10, 20, 30)

# Desempaquetar diccionario con **
def crear_usuario(nombre, edad, ciudad):
    return f"{nombre}, {edad} años, {ciudad}"

datos = {"nombre": "Juan", "edad": 30, "ciudad": "Madrid"}
usuario = crear_usuario(**datos)  # Equivale a: crear_usuario(nombre="Juan", edad=30, ciudad="Madrid")
```

### 2.7 Argumentos Solo Posicionales y Solo Nombrados (Python 3.8+)

```python
def funcion(a, b, /, c, d, *, e, f):
    """
    a, b: solo posicionales (antes de /)
    c, d: pueden ser posicionales o nombrados
    e, f: solo nombrados (después de *)
    """
    return a + b + c + d + e + f

# Válido
funcion(1, 2, 3, 4, e=5, f=6)
funcion(1, 2, c=3, d=4, e=5, f=6)

# Inválido
# funcion(a=1, b=2, c=3, d=4, e=5, f=6)  # Error: a y b solo posicionales
# funcion(1, 2, 3, 4, 5, 6)  # Error: e y f solo nombrados
```

---

## 3. Lambdas

Funciones anónimas de una sola expresión.

### 3.1 Sintaxis Básica

```python
# Función normal
def cuadrado(x):
    return x ** 2

# Equivalente con lambda
cuadrado_lambda = lambda x: x ** 2

print(cuadrado(5))  # 25
print(cuadrado_lambda(5))  # 25
```

### 3.2 Lambdas con Múltiples Argumentos

```python
sumar = lambda a, b: a + b
print(sumar(10, 20))  # 30

# Lambda con condicional
maximo = lambda a, b: a if a > b else b
print(maximo(10, 20))  # 20
```

### 3.3 Uso Común: Funciones de Orden Superior

```python
# map()
numeros = [1, 2, 3, 4, 5]
cuadrados = list(map(lambda x: x ** 2, numeros))
print(cuadrados)  # [1, 4, 9, 16, 25]

# filter()
pares = list(filter(lambda x: x % 2 == 0, numeros))
print(pares)  # [2, 4]

# sorted() con key
personas = [
    {"nombre": "Juan", "edad": 30},
    {"nombre": "Ana", "edad": 25},
    {"nombre": "Pedro", "edad": 35}
]
ordenadas = sorted(personas, key=lambda p: p["edad"])
print([p["nombre"] for p in ordenadas])  # ['Ana', 'Juan', 'Pedro']
```

### 3.4 Cuándo NO Usar Lambdas

```python
# ❌ MAL: Lambda compleja
calcular = lambda x, y: x ** 2 + y ** 2 if x > 0 and y > 0 else 0

# ✅ BIEN: Función normal para lógica compleja
def calcular(x, y):
    if x > 0 and y > 0:
        return x ** 2 + y ** 2
    return 0
```

---

## 4. Closures

Una closure es una función que "recuerda" variables del scope exterior.

### 4.1 Concepto Básico

```python
def crear_multiplicador(factor):
    """Retorna una función que multiplica por factor."""
    def multiplicar(numero):
        return numero * factor  # 'factor' viene del scope exterior
    return multiplicar

por_dos = crear_multiplicador(2)
por_tres = crear_multiplicador(3)

print(por_dos(10))  # 20
print(por_tres(10))  # 30
```

### 4.2 Closures con Estado

```python
def crear_contador(inicial=0):
    """Crea un contador con estado."""
    contador = inicial

    def incrementar():
        nonlocal contador  # Modificar variable del scope exterior
        contador += 1
        return contador

    return incrementar

contador1 = crear_contador()
print(contador1())  # 1
print(contador1())  # 2
print(contador1())  # 3

contador2 = crear_contador(100)
print(contador2())  # 101
print(contador2())  # 102
```

### 4.3 Factory Functions

```python
def crear_saludador(saludo):
    """Factory de funciones saludadoras."""
    def saludar(nombre):
        return f"{saludo}, {nombre}!"
    return saludar

hola = crear_saludador("Hola")
buenos_dias = crear_saludador("Buenos días")

print(hola("Ana"))  # "Hola, Ana!"
print(buenos_dias("Pedro"))  # "Buenos días, Pedro!"
```

### 4.4 Closures vs Clases

```python
# Con closure
def crear_calculadora(operacion):
    def calcular(a, b):
        if operacion == "sumar":
            return a + b
        elif operacion == "restar":
            return a - b
    return calcular

# Con clase
class Calculadora:
    def __init__(self, operacion):
        self.operacion = operacion

    def calcular(self, a, b):
        if self.operacion == "sumar":
            return a + b
        elif self.operacion == "restar":
            return a - b

# Uso similar
suma_closure = crear_calculadora("sumar")
suma_clase = Calculadora("sumar")

print(suma_closure(10, 5))  # 15
print(suma_clase.calcular(10, 5))  # 15
```

---

## 5. Decoradores

Un decorador es una función que modifica el comportamiento de otra función.

### 5.1 Decorador Básico

```python
def mi_decorador(func):
    """Decorador simple que imprime antes y después."""
    def wrapper():
        print("Antes de ejecutar")
        func()
        print("Después de ejecutar")
    return wrapper

@mi_decorador
def saludar():
    print("¡Hola!")

saludar()
# Antes de ejecutar
# ¡Hola!
# Después de ejecutar

# Equivale a:
# saludar = mi_decorador(saludar)
```

### 5.2 Decorador con Argumentos en la Función

```python
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        print(f"Llamando a {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"Resultado: {resultado}")
        return resultado
    return wrapper

@mi_decorador
def sumar(a, b):
    return a + b

sumar(10, 20)
# Llamando a sumar
# Resultado: 30
```

### 5.3 Decorador con Parámetros

```python
def repetir(veces):
    """Decorador que repite la ejecución n veces."""
    def decorador(func):
        def wrapper(*args, **kwargs):
            for _ in range(veces):
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador

@repetir(3)
def saludar(nombre):
    print(f"Hola, {nombre}!")
    return True

saludar("Ana")
# Hola, Ana!
# Hola, Ana!
# Hola, Ana!
```

### 5.4 Decoradores Útiles

#### a) Medir Tiempo de Ejecución

```python
import time
from functools import wraps

def medir_tiempo(func):
    """Mide el tiempo de ejecución de una función."""
    @wraps(func)  # Preserva metadata de func
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"{func.__name__} tardó {fin - inicio:.4f} segundos")
        return resultado
    return wrapper

@medir_tiempo
def procesar_datos():
    time.sleep(1)
    return "Datos procesados"

procesar_datos()
# procesar_datos tardó 1.0012 segundos
```

#### b) Cachear Resultados

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    """Calcula Fibonacci con caché."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Rápido gracias al caché
```

#### c) Validar Tipos

```python
def validar_tipos(*tipos_esperados):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg, tipo in zip(args, tipos_esperados):
                if not isinstance(arg, tipo):
                    raise TypeError(f"Esperaba {tipo}, recibió {type(arg)}")
            return func(*args, **kwargs)
        return wrapper
    return decorador

@validar_tipos(int, int)
def sumar(a, b):
    return a + b

print(sumar(10, 20))  # 30
# print(sumar(10, "20"))  # TypeError
```

### 5.5 Múltiples Decoradores

```python
def negrita(func):
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper

def cursiva(func):
    def wrapper():
        return "<i>" + func() + "</i>"
    return wrapper

@negrita
@cursiva
def texto():
    return "Hola"

print(texto())  # <b><i>Hola</i></b>

# Orden de aplicación (de abajo hacia arriba):
# 1. cursiva(texto)
# 2. negrita(resultado_anterior)
```

### 5.6 Decoradores de Clase

```python
def singleton(cls):
    """Decorador que convierte una clase en Singleton."""
    instancias = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instancias:
            instancias[cls] = cls(*args, **kwargs)
        return instancias[cls]

    return get_instance

@singleton
class BaseDatos:
    def __init__(self):
        print("Conectando a base de datos...")

db1 = BaseDatos()  # Conectando a base de datos...
db2 = BaseDatos()  # No imprime (usa la misma instancia)
print(db1 is db2)  # True
```

---

## 6. Iteradores

Un iterador es un objeto que implementa `__iter__()` y `__next__()`.

### 6.1 Protocolo de Iterador

```python
# Las listas son iterables
numeros = [1, 2, 3]

# Obtener iterador
iterador = iter(numeros)

# Iterar manualmente
print(next(iterador))  # 1
print(next(iterador))  # 2
print(next(iterador))  # 3
# print(next(iterador))  # StopIteration

# El for usa iteradores internamente
for numero in numeros:
    print(numero)
```

### 6.2 Crear Iterador Personalizado

```python
class Contador:
    """Iterador que cuenta desde inicio hasta fin."""

    def __init__(self, inicio, fin):
        self.actual = inicio
        self.fin = fin

    def __iter__(self):
        return self

    def __next__(self):
        if self.actual > self.fin:
            raise StopIteration
        numero = self.actual
        self.actual += 1
        return numero

# Uso
for num in Contador(1, 5):
    print(num)
# 1, 2, 3, 4, 5
```

### 6.3 Itertools - Herramientas para Iteradores

```python
import itertools

# count - contador infinito
contador = itertools.count(start=10, step=2)
print(next(contador))  # 10
print(next(contador))  # 12

# cycle - repite secuencia infinitamente
colores = itertools.cycle(['rojo', 'verde', 'azul'])
print(next(colores))  # rojo
print(next(colores))  # verde

# chain - concatena iterables
resultado = list(itertools.chain([1, 2], [3, 4], [5, 6]))
print(resultado)  # [1, 2, 3, 4, 5, 6]

# islice - slice de iterador
numeros = range(100)
primeros_10 = list(itertools.islice(numeros, 10))
print(primeros_10)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# combinations - combinaciones
items = ['A', 'B', 'C']
combos = list(itertools.combinations(items, 2))
print(combos)  # [('A', 'B'), ('A', 'C'), ('B', 'C')]

# permutations - permutaciones
perms = list(itertools.permutations(items, 2))
print(perms)  # [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]
```

---

## 7. Generadores

Los generadores son una forma simple de crear iteradores usando `yield`.

### 7.1 Función Generadora

```python
def contador(inicio, fin):
    """Generador que cuenta desde inicio hasta fin."""
    while inicio <= fin:
        yield inicio  # Pausa la función y retorna valor
        inicio += 1

# Uso
for num in contador(1, 5):
    print(num)
# 1, 2, 3, 4, 5

# Es un generador
gen = contador(1, 3)
print(type(gen))  # <class 'generator'>
print(next(gen))  # 1
print(next(gen))  # 2
```

### 7.2 Ventajas de Generadores

Los generadores son eficientes en memoria:

```python
# ❌ Lista - carga todo en memoria
def numeros_lista(n):
    resultado = []
    for i in range(n):
        resultado.append(i ** 2)
    return resultado

# ✅ Generador - genera valores bajo demanda
def numeros_generador(n):
    for i in range(n):
        yield i ** 2

# Comparación
import sys
lista = numeros_lista(1000)
gen = numeros_generador(1000)

print(sys.getsizeof(lista))  # ~9000 bytes
print(sys.getsizeof(gen))    # ~128 bytes
```

### 7.3 yield from

Delega a otro generador:

```python
def generador1():
    yield 1
    yield 2

def generador2():
    yield 3
    yield 4

def generador_combinado():
    yield from generador1()
    yield from generador2()

print(list(generador_combinado()))  # [1, 2, 3, 4]

# Útil para aplanar listas
def aplanar(lista):
    for item in lista:
        if isinstance(item, list):
            yield from aplanar(item)  # Recursivo
        else:
            yield item

anidada = [1, [2, 3, [4, 5]], 6]
print(list(aplanar(anidada)))  # [1, 2, 3, 4, 5, 6]
```

### 7.4 Expresiones Generadoras

Similar a list comprehension, pero con paréntesis:

```python
# List comprehension - crea lista
cuadrados_lista = [x ** 2 for x in range(10)]

# Expresión generadora - crea generador
cuadrados_gen = (x ** 2 for x in range(10))

print(type(cuadrados_lista))  # <class 'list'>
print(type(cuadrados_gen))    # <class 'generator'>

# Uso
print(sum(cuadrados_gen))  # 285
```

### 7.5 Generadores con send()

Los generadores pueden recibir valores:

```python
def acumulador():
    """Generador que acumula valores."""
    total = 0
    while True:
        valor = yield total  # Retorna total y recibe valor
        if valor is not None:
            total += valor

gen = acumulador()
print(next(gen))  # 0 (inicializar)
print(gen.send(10))  # 10
print(gen.send(20))  # 30
print(gen.send(5))   # 35
```

---

## 8. Comprensiones

### 8.1 List Comprehension

```python
# Forma tradicional
cuadrados = []
for x in range(10):
    cuadrados.append(x ** 2)

# List comprehension
cuadrados = [x ** 2 for x in range(10)]

# Con condicional
pares = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# Con if-else
numeros = [x if x % 2 == 0 else -x for x in range(5)]
# [0, -1, 2, -3, 4]

# Anidadas
matriz = [[i * j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
```

### 8.2 Dict Comprehension

```python
# Crear diccionario
cuadrados = {x: x ** 2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Invertir diccionario
original = {'a': 1, 'b': 2, 'c': 3}
invertido = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Con condicional
pares = {x: x ** 2 for x in range(10) if x % 2 == 0}
# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
```

### 8.3 Set Comprehension

```python
# Crear set
cuadrados = {x ** 2 for x in range(-5, 6)}
# {0, 1, 4, 9, 16, 25}  (sin duplicados)

# Letras únicas
texto = "abracadabra"
letras = {c for c in texto}
# {'a', 'b', 'r', 'c', 'd'}
```

### 8.4 Cuándo NO Usar Comprensiones

```python
# ❌ MAL: Comprensión compleja (difícil de leer)
resultado = [
    x ** 2 if x % 2 == 0 else x ** 3
    for x in range(100)
    if x > 10 and x < 50 or x % 7 == 0
]

# ✅ BIEN: Bucle tradicional para lógica compleja
resultado = []
for x in range(100):
    if (x > 10 and x < 50) or x % 7 == 0:
        if x % 2 == 0:
            resultado.append(x ** 2)
        else:
            resultado.append(x ** 3)
```

---

## 9. Context Managers

Context managers gestionan recursos automáticamente usando `with`.

### 9.1 Uso con Archivos

```python
# ❌ Sin context manager
archivo = open('datos.txt', 'w')
try:
    archivo.write('Hola')
finally:
    archivo.close()

# ✅ Con context manager
with open('datos.txt', 'w') as archivo:
    archivo.write('Hola')
# archivo.close() se llama automáticamente
```

### 9.2 Crear Context Manager con Clase

```python
class MiContextManager:
    """Context manager personalizado."""

    def __enter__(self):
        """Ejecutado al entrar al bloque with."""
        print("Entrando al contexto")
        return self  # Valor asignado a 'as variable'

    def __exit__(self, exc_type, exc_value, traceback):
        """Ejecutado al salir del bloque with."""
        print("Saliendo del contexto")
        if exc_type is not None:
            print(f"Ocurrió error: {exc_value}")
        return False  # False = propaga la excepción

# Uso
with MiContextManager() as cm:
    print("Dentro del bloque with")
# Entrando al contexto
# Dentro del bloque with
# Saliendo del contexto
```

### 9.3 Context Manager de Temporización

```python
import time

class Temporizador:
    """Context manager que mide tiempo de ejecución."""

    def __enter__(self):
        self.inicio = time.time()
        return self

    def __exit__(self, *args):
        self.fin = time.time()
        self.duracion = self.fin - self.inicio
        print(f"Duración: {self.duracion:.4f} segundos")
        return False

# Uso
with Temporizador():
    time.sleep(1)
    print("Procesando...")
# Procesando...
# Duración: 1.0012 segundos
```

### 9.4 Context Manager con contextlib

```python
from contextlib import contextmanager

@contextmanager
def mi_contexto():
    """Context manager usando generador."""
    print("Preparando")
    try:
        yield "Valor del contexto"
    finally:
        print("Limpiando")

# Uso
with mi_contexto() as valor:
    print(f"Usando: {valor}")
# Preparando
# Usando: Valor del contexto
# Limpiando
```

### 9.5 Context Manager de Conexión a BD

```python
@contextmanager
def conexion_bd(host, usuario, password):
    """Maneja conexión a base de datos."""
    # Setup
    conexion = conectar(host, usuario, password)
    print("Conectado a BD")

    try:
        yield conexion
    finally:
        # Cleanup
        conexion.cerrar()
        print("Desconectado de BD")

# Uso
with conexion_bd("localhost", "user", "pass") as conn:
    conn.ejecutar("SELECT * FROM usuarios")
```

### 9.6 Múltiples Context Managers

```python
# Forma tradicional
with open('entrada.txt') as entrada:
    with open('salida.txt', 'w') as salida:
        for linea in entrada:
            salida.write(linea.upper())

# Forma abreviada (Python 3.1+)
with open('entrada.txt') as entrada, open('salida.txt', 'w') as salida:
    for linea in entrada:
        salida.write(linea.upper())
```

---

## 10. Programación Pythonic

### 10.1 Zen de Python

```python
import this
```

Principios clave:
- Explícito es mejor que implícito
- Simple es mejor que complejo
- Legibilidad cuenta
- Los casos especiales no son tan especiales como para romper las reglas

### 10.2 Idiomas Pythonic

#### Intercambiar Variables

```python
# ❌ No pythonic
temp = a
a = b
b = temp

# ✅ Pythonic
a, b = b, a
```

#### Iterar con Índice

```python
items = ['a', 'b', 'c']

# ❌ No pythonic
for i in range(len(items)):
    print(f"{i}: {items[i]}")

# ✅ Pythonic
for i, item in enumerate(items):
    print(f"{i}: {item}")
```

#### Iterar sobre Dos Listas

```python
nombres = ['Ana', 'Juan', 'Pedro']
edades = [25, 30, 35]

# ❌ No pythonic
for i in range(len(nombres)):
    print(f"{nombres[i]}: {edades[i]}")

# ✅ Pythonic
for nombre, edad in zip(nombres, edades):
    print(f"{nombre}: {edad}")
```

#### Verificar Existencia

```python
# ❌ No pythonic
if len(lista) > 0:
    pass

# ✅ Pythonic
if lista:
    pass
```

#### Valores por Defecto de Diccionario

```python
# ❌ No pythonic
if 'clave' in diccionario:
    valor = diccionario['clave']
else:
    valor = 'default'

# ✅ Pythonic
valor = diccionario.get('clave', 'default')
```

### 10.3 EAFP vs LBYL

**LBYL** (Look Before You Leap) - Verificar antes:
```python
# LBYL
if 'clave' in diccionario:
    valor = diccionario['clave']
```

**EAFP** (Easier to Ask for Forgiveness than Permission) - Pythonic:
```python
# EAFP (más pythonic)
try:
    valor = diccionario['clave']
except KeyError:
    valor = None
```

### 10.4 Duck Typing

"Si camina como pato y grazna como pato, entonces es un pato"

```python
# No verificamos el tipo, sino las capacidades
def procesar(iterable):
    """Funciona con cualquier iterable."""
    for item in iterable:
        print(item)

procesar([1, 2, 3])  # Lista
procesar((1, 2, 3))  # Tupla
procesar({1, 2, 3})  # Set
procesar("abc")      # String
```

### 10.5 List/Dict/Set Comprehensions

```python
# ❌ No pythonic
cuadrados = []
for x in range(10):
    cuadrados.append(x ** 2)

# ✅ Pythonic
cuadrados = [x ** 2 for x in range(10)]
```

### 10.6 Uso de with para Recursos

```python
# ❌ No pythonic
archivo = open('datos.txt')
try:
    contenido = archivo.read()
finally:
    archivo.close()

# ✅ Pythonic
with open('datos.txt') as archivo:
    contenido = archivo.read()
```

---

## Resumen

En este módulo has aprendido:

✅ **Funciones**: Definición, argumentos, retorno múltiple, first-class objects
✅ **Argumentos**: Posicionales, nombrados, *args, **kwargs, desempaquetado
✅ **Lambdas**: Funciones anónimas, uso con map/filter/sorted
✅ **Closures**: Funciones que recuerdan variables externas, factory functions
✅ **Decoradores**: Modificar comportamiento de funciones, decoradores con parámetros
✅ **Iteradores**: Protocolo iter/next, itertools
✅ **Generadores**: yield, expresiones generadoras, eficiencia en memoria
✅ **Comprensiones**: List, dict, set comprehensions
✅ **Context Managers**: with, __enter__/__exit__, contextlib
✅ **Programación Pythonic**: Idiomas, EAFP, duck typing

## Recursos Adicionales

- [PEP 8 - Style Guide](https://pep8.org/)
- [PEP 20 - Zen of Python](https://www.python.org/dev/peps/pep-0020/)
- [Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [Itertools](https://docs.python.org/3/library/itertools.html)
- [contextlib](https://docs.python.org/3/library/contextlib.html)

---

**Próximo paso:** Completar el laboratorio práctico con decoradores, generadores y context managers.
