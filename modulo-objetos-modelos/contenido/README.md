# Módulo 4: Objetos y Modelos de Datos

## Índice

1. [Clases en Python](#1-clases-en-python)
2. [Herencia](#2-herencia)
3. [Composición](#3-composición)
4. [Dunder Methods (Métodos Mágicos)](#4-dunder-methods-métodos-mágicos)
5. [Dataclasses](#5-dataclasses)
6. [Attrs](#6-attrs)
7. [Pydantic](#7-pydantic)
8. [Comparación de Herramientas](#8-comparación-de-herramientas)

---

## 1. Clases en Python

### 1.1 Definición Básica

```python
class Persona:
    """Representa una persona con nombre y edad."""

    def __init__(self, nombre: str, edad: int):
        """Constructor de la clase."""
        self.nombre = nombre
        self.edad = edad

    def saludar(self) -> str:
        """Retorna un saludo personalizado."""
        return f"Hola, soy {self.nombre} y tengo {self.edad} años"

# Uso
persona = Persona("Juan", 30)
print(persona.saludar())  # "Hola, soy Juan y tengo 30 años"
```

### 1.2 Atributos de Clase vs Instancia

```python
class Contador:
    # Atributo de clase (compartido por todas las instancias)
    total_instancias = 0

    def __init__(self, nombre: str):
        # Atributo de instancia (único para cada objeto)
        self.nombre = nombre
        self.valor = 0
        Contador.total_instancias += 1

    def incrementar(self):
        self.valor += 1

# Uso
c1 = Contador("C1")
c2 = Contador("C2")
print(Contador.total_instancias)  # 2

c1.incrementar()
print(c1.valor)  # 1
print(c2.valor)  # 0 (independiente)
```

### 1.3 Métodos de Clase y Estáticos

```python
from datetime import datetime

class Persona:
    def __init__(self, nombre: str, año_nacimiento: int):
        self.nombre = nombre
        self.año_nacimiento = año_nacimiento

    @classmethod
    def desde_edad(cls, nombre: str, edad: int):
        """Factory method: crea instancia desde edad."""
        año_actual = datetime.now().year
        return cls(nombre, año_actual - edad)

    @staticmethod
    def es_mayor_de_edad(edad: int) -> bool:
        """Método estático: no accede a self ni cls."""
        return edad >= 18

    @property
    def edad(self) -> int:
        """Property: calcula edad dinámicamente."""
        return datetime.now().year - self.año_nacimiento

# Uso
p1 = Persona("Ana", 1995)
p2 = Persona.desde_edad("Pedro", 25)  # Factory method

print(p1.edad)  # Property (sin paréntesis)
print(Persona.es_mayor_de_edad(20))  # True
```

### 1.4 Encapsulación

```python
class CuentaBancaria:
    def __init__(self, titular: str, saldo_inicial: float = 0):
        self.titular = titular
        self._saldo = saldo_inicial  # Convención: "privado"
        self.__pin = "1234"  # Name mangling: muy privado

    @property
    def saldo(self) -> float:
        """Getter para saldo."""
        return self._saldo

    def depositar(self, monto: float):
        """Depositar dinero."""
        if monto > 0:
            self._saldo += monto
        else:
            raise ValueError("Monto debe ser positivo")

    def retirar(self, monto: float):
        """Retirar dinero."""
        if monto > self._saldo:
            raise ValueError("Saldo insuficiente")
        self._saldo -= monto

# Uso
cuenta = CuentaBancaria("Juan", 1000)
print(cuenta.saldo)  # 1000
cuenta.depositar(500)
cuenta.retirar(200)
print(cuenta.saldo)  # 1300

# cuenta._saldo = 9999  # ❌ Técnicamente posible, pero mala práctica
```

---

## 2. Herencia

### 2.1 Herencia Simple

```python
class Animal:
    """Clase base."""

    def __init__(self, nombre: str):
        self.nombre = nombre

    def hacer_sonido(self) -> str:
        return "Sonido genérico"

class Perro(Animal):
    """Clase derivada."""

    def hacer_sonido(self) -> str:
        return "Guau!"

class Gato(Animal):
    def hacer_sonido(self) -> str:
        return "Miau!"

# Uso
animales = [Perro("Firulais"), Gato("Mishi"), Animal("Genérico")]
for animal in animales:
    print(f"{animal.nombre}: {animal.hacer_sonido()}")
# Firulais: Guau!
# Mishi: Miau!
# Genérico: Sonido genérico
```

### 2.2 super() y MRO (Method Resolution Order)

```python
class Vehiculo:
    def __init__(self, marca: str):
        self.marca = marca
        print(f"Inicializando Vehiculo: {marca}")

class Electrico:
    def __init__(self, bateria: int):
        self.bateria = bateria
        print(f"Inicializando Electrico: {bateria}kWh")

class Auto(Vehiculo):
    def __init__(self, marca: str, modelo: str):
        super().__init__(marca)  # Llama a Vehiculo.__init__
        self.modelo = modelo
        print(f"Inicializando Auto: {modelo}")

# Uso
auto = Auto("Tesla", "Model 3")
# Inicializando Vehiculo: Tesla
# Inicializando Auto: Model 3
```

### 2.3 Herencia Múltiple

```python
class Volador:
    def volar(self):
        return "Estoy volando"

class Nadador:
    def nadar(self):
        return "Estoy nadando"

class Pato(Volador, Nadador):
    """Herencia múltiple."""
    def __init__(self, nombre: str):
        self.nombre = nombre

# Uso
pato = Pato("Donald")
print(pato.volar())  # "Estoy volando"
print(pato.nadar())  # "Estoy nadando"

# Ver el MRO (Method Resolution Order)
print(Pato.__mro__)
# (<class 'Pato'>, <class 'Volador'>, <class 'Nadador'>, <class 'object'>)
```

### 2.4 Clases Abstractas

```python
from abc import ABC, abstractmethod

class Forma(ABC):
    """Clase abstracta base."""

    @abstractmethod
    def area(self) -> float:
        """Método abstracto que debe ser implementado."""
        pass

    @abstractmethod
    def perimetro(self) -> float:
        pass

class Rectangulo(Forma):
    def __init__(self, ancho: float, alto: float):
        self.ancho = ancho
        self.alto = alto

    def area(self) -> float:
        return self.ancho * self.alto

    def perimetro(self) -> float:
        return 2 * (self.ancho + self.alto)

class Circulo(Forma):
    def __init__(self, radio: float):
        self.radio = radio

    def area(self) -> float:
        import math
        return math.pi * self.radio ** 2

    def perimetro(self) -> float:
        import math
        return 2 * math.pi * self.radio

# Uso
# forma = Forma()  # ❌ TypeError: No se puede instanciar clase abstracta
rectangulo = Rectangulo(5, 3)
print(f"Área: {rectangulo.area()}")  # 15
```

---

## 3. Composición

### 3.1 Composición vs Herencia

**Herencia:** "es un" (is-a)
**Composición:** "tiene un" (has-a)

```python
# ❌ MAL: Abuso de herencia
class Motor:
    def arrancar(self):
        return "Motor arrancado"

class Auto(Motor):  # Auto "es un" Motor? No tiene sentido
    pass

# ✅ BIEN: Composición
class Motor:
    def arrancar(self):
        return "Motor arrancado"

class Auto:
    def __init__(self):
        self.motor = Motor()  # Auto "tiene un" Motor

    def arrancar(self):
        return self.motor.arrancar()
```

### 3.2 Ejemplo Completo de Composición

```python
class Motor:
    def __init__(self, cilindros: int, potencia: int):
        self.cilindros = cilindros
        self.potencia = potencia
        self.encendido = False

    def arrancar(self):
        self.encendido = True
        return f"Motor de {self.cilindros} cilindros arrancado"

    def detener(self):
        self.encendido = False

class Rueda:
    def __init__(self, tamaño: int):
        self.tamaño = tamaño
        self.desgaste = 0

class Auto:
    def __init__(self, marca: str, modelo: str):
        self.marca = marca
        self.modelo = modelo
        self.motor = Motor(4, 150)
        self.ruedas = [Rueda(17) for _ in range(4)]

    def arrancar(self):
        return self.motor.arrancar()

    def info(self):
        return f"{self.marca} {self.modelo} - Motor: {self.motor.potencia}hp"

# Uso
auto = Auto("Toyota", "Corolla")
print(auto.arrancar())
print(auto.info())
```

---

## 4. Dunder Methods (Métodos Mágicos)

Métodos especiales con doble guión bajo que Python llama automáticamente.

### 4.1 Métodos de Representación

```python
class Producto:
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio

    def __str__(self) -> str:
        """Para print() y str() - legible para humanos."""
        return f"{self.nombre} - ${self.precio:.2f}"

    def __repr__(self) -> str:
        """Para repr() y consola - para desarrolladores."""
        return f"Producto(nombre='{self.nombre}', precio={self.precio})"

# Uso
p = Producto("Laptop", 1200.50)
print(p)  # Laptop - $1200.50 (usa __str__)
print(repr(p))  # Producto(nombre='Laptop', precio=1200.5) (usa __repr__)
```

### 4.2 Métodos de Comparación

```python
class Persona:
    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre
        self.edad = edad

    def __eq__(self, other) -> bool:
        """Igualdad (==)."""
        if not isinstance(other, Persona):
            return NotImplemented
        return self.edad == other.edad

    def __lt__(self, other) -> bool:
        """Menor que (<)."""
        if not isinstance(other, Persona):
            return NotImplemented
        return self.edad < other.edad

    def __le__(self, other) -> bool:
        """Menor o igual (<=)."""
        return self < other or self == other

# Uso
p1 = Persona("Ana", 25)
p2 = Persona("Juan", 30)

print(p1 == p2)  # False
print(p1 < p2)   # True
print(sorted([p2, p1], key=lambda p: p.edad))  # Ordena por edad
```

### 4.3 Métodos Aritméticos

```python
class Dinero:
    def __init__(self, cantidad: float, moneda: str = "USD"):
        self.cantidad = cantidad
        self.moneda = moneda

    def __add__(self, other):
        """Suma (+)."""
        if isinstance(other, Dinero):
            if self.moneda != other.moneda:
                raise ValueError("No se pueden sumar monedas diferentes")
            return Dinero(self.cantidad + other.cantidad, self.moneda)
        return Dinero(self.cantidad + other, self.moneda)

    def __sub__(self, other):
        """Resta (-)."""
        if isinstance(other, Dinero):
            if self.moneda != other.moneda:
                raise ValueError("No se pueden restar monedas diferentes")
            return Dinero(self.cantidad - other.cantidad, self.moneda)
        return Dinero(self.cantidad - other, self.moneda)

    def __mul__(self, factor):
        """Multiplicación (*)."""
        return Dinero(self.cantidad * factor, self.moneda)

    def __str__(self):
        return f"{self.cantidad:.2f} {self.moneda}"

# Uso
d1 = Dinero(100)
d2 = Dinero(50)
print(d1 + d2)  # 150.00 USD
print(d1 * 2)   # 200.00 USD
```

### 4.4 Métodos de Contenedor

```python
class Inventario:
    def __init__(self):
        self._items = {}

    def __len__(self):
        """len(inventario)."""
        return len(self._items)

    def __getitem__(self, key):
        """inventario[key]."""
        return self._items[key]

    def __setitem__(self, key, value):
        """inventario[key] = value."""
        self._items[key] = value

    def __delitem__(self, key):
        """del inventario[key]."""
        del self._items[key]

    def __contains__(self, key):
        """key in inventario."""
        return key in self._items

    def __iter__(self):
        """for item in inventario."""
        return iter(self._items)

# Uso
inv = Inventario()
inv["laptop"] = 10
inv["mouse"] = 50
print(len(inv))  # 2
print("laptop" in inv)  # True
for item in inv:
    print(item)
```

### 4.5 Context Manager

```python
class ArchivoLog:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.archivo = None

    def __enter__(self):
        """Llamado al entrar al with."""
        self.archivo = open(self.nombre, 'w')
        return self.archivo

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Llamado al salir del with."""
        if self.archivo:
            self.archivo.close()
        return False  # No suprime excepciones

# Uso
with ArchivoLog("log.txt") as f:
    f.write("Mensaje de log\n")
# El archivo se cierra automáticamente
```

---

## 5. Dataclasses

Introducidas en Python 3.7, simplifican la creación de clases de datos.

### 5.1 Básico

```python
from dataclasses import dataclass

@dataclass
class Persona:
    nombre: str
    edad: int
    ciudad: str = "Desconocida"  # Valor por defecto

# Genera automáticamente:
# - __init__
# - __repr__
# - __eq__

# Uso
p1 = Persona("Ana", 25)
p2 = Persona("Ana", 25, "Madrid")
print(p1)  # Persona(nombre='Ana', edad=25, ciudad='Desconocida')
print(p1 == p2)  # False (ciudad diferente)
```

### 5.2 Opciones de @dataclass

```python
from dataclasses import dataclass, field

@dataclass(
    frozen=True,  # Inmutable
    order=True,   # Genera __lt__, __le__, __gt__, __ge__
)
class Punto:
    x: float
    y: float

# Inmutable
p = Punto(1, 2)
# p.x = 10  # ❌ Error: no se puede modificar

# Ordenable
puntos = [Punto(3, 4), Punto(1, 2), Punto(2, 3)]
print(sorted(puntos))  # Ordena por (x, y)
```

### 5.3 field() para Configuración Avanzada

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Producto:
    nombre: str
    precio: float
    categorias: List[str] = field(default_factory=list)  # Lista mutable
    _inventario: int = field(default=0, repr=False)  # No en repr
    id: int = field(init=False)  # No en __init__

    def __post_init__(self):
        """Llamado después de __init__."""
        import random
        self.id = random.randint(1000, 9999)

# Uso
p1 = Producto("Laptop", 1200)
p2 = Producto("Mouse", 25, ["accesorios"])
print(p1)  # Producto(nombre='Laptop', precio=1200, categorias=[], id=1234)
```

### 5.4 Métodos Personalizados

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Carrito:
    items: List[dict] = field(default_factory=list)

    def agregar(self, producto: str, precio: float, cantidad: int = 1):
        """Agregar producto al carrito."""
        self.items.append({
            "producto": producto,
            "precio": precio,
            "cantidad": cantidad
        })

    @property
    def total(self) -> float:
        """Calcular total del carrito."""
        return sum(item["precio"] * item["cantidad"] for item in self.items)

    @property
    def cantidad_items(self) -> int:
        """Total de items."""
        return sum(item["cantidad"] for item in self.items)

# Uso
carrito = Carrito()
carrito.agregar("Laptop", 1200, 1)
carrito.agregar("Mouse", 25, 2)
print(f"Total: ${carrito.total}")  # Total: $1250
print(f"Items: {carrito.cantidad_items}")  # Items: 3
```

---

## 6. Attrs

Biblioteca alternativa a dataclasses con más funcionalidades.

### 6.1 Básico

```python
import attrs

@attrs.define
class Persona:
    nombre: str
    edad: int
    ciudad: str = "Desconocida"

# Uso (similar a dataclasses)
p = Persona("Ana", 25)
print(p)  # Persona(nombre='Ana', edad=25, ciudad='Desconocida')
```

### 6.2 Validadores

```python
import attrs
from attrs import validators

@attrs.define
class Usuario:
    username: str = attrs.field(validator=validators.instance_of(str))
    edad: int = attrs.field(validator=validators.and_(
        validators.instance_of(int),
        validators.ge(0),  # >= 0
        validators.le(150)  # <= 150
    ))
    email: str = attrs.field(validator=validators.matches_re(r'^[\w\.-]+@[\w\.-]+\.\w+$'))

# Uso
usuario = Usuario("john_doe", 25, "john@example.com")  # ✅ OK
# usuario = Usuario("john", 200, "invalid")  # ❌ Error de validación
```

### 6.3 Conversores

```python
import attrs

@attrs.define
class Producto:
    nombre: str
    precio: float = attrs.field(converter=float)  # Convierte a float automáticamente

# Uso
p = Producto("Laptop", "1200.50")  # String se convierte a float
print(type(p.precio))  # <class 'float'>
print(p.precio)  # 1200.5
```

---

## 7. Pydantic

Biblioteca para validación de datos y serialización con type hints.

### 7.1 Modelo Básico

```python
from pydantic import BaseModel

class Usuario(BaseModel):
    nombre: str
    edad: int
    email: str

# Validación automática
usuario = Usuario(nombre="Ana", edad=25, email="ana@example.com")
print(usuario)  # nombre='Ana' edad=25 email='ana@example.com'

# Conversión de tipos
usuario2 = Usuario(nombre="Juan", edad="30", email="juan@example.com")
print(type(usuario2.edad))  # <class 'int'> (convertido desde string)

# Validación de errores
try:
    Usuario(nombre="Pedro", edad="invalid", email="pedro@example.com")
except Exception as e:
    print(f"Error: {e}")
```

### 7.2 Validadores Personalizados

```python
from pydantic import BaseModel, validator, field_validator
from typing import Optional

class Usuario(BaseModel):
    username: str
    edad: int
    email: str

    @field_validator('username')
    @classmethod
    def validar_username(cls, v):
        """Username debe tener al menos 3 caracteres."""
        if len(v) < 3:
            raise ValueError('Username debe tener al menos 3 caracteres')
        return v.lower()  # Convertir a minúsculas

    @field_validator('edad')
    @classmethod
    def validar_edad(cls, v):
        """Edad debe estar entre 0 y 150."""
        if not 0 <= v <= 150:
            raise ValueError('Edad debe estar entre 0 y 150')
        return v

# Uso
usuario = Usuario(username="JohnDoe", edad=25, email="john@example.com")
print(usuario.username)  # johndoe (convertido a minúsculas)
```

### 7.3 Validadores de Modelo

```python
from pydantic import BaseModel, model_validator

class Rango(BaseModel):
    minimo: int
    maximo: int

    @model_validator(mode='after')
    def validar_rango(self):
        """Validador que usa múltiples campos."""
        if self.minimo >= self.maximo:
            raise ValueError('minimo debe ser menor que maximo')
        return self

# Uso
r1 = Rango(minimo=1, maximo=10)  # ✅ OK
# r2 = Rango(minimo=10, maximo=5)  # ❌ Error
```

### 7.4 Serialización

```python
from pydantic import BaseModel
from datetime import datetime

class Evento(BaseModel):
    nombre: str
    fecha: datetime
    participantes: int

# Crear desde dict
data = {
    "nombre": "Conferencia Python",
    "fecha": "2024-06-15T10:00:00",
    "participantes": 100
}
evento = Evento(**data)

# Serializar a dict
print(evento.model_dump())
# {'nombre': 'Conferencia Python', 'fecha': datetime(...), 'participantes': 100}

# Serializar a JSON
print(evento.model_dump_json())
# '{"nombre":"Conferencia Python","fecha":"2024-06-15T10:00:00","participantes":100}'
```

### 7.5 Modelos Anidados

```python
from pydantic import BaseModel
from typing import List

class Direccion(BaseModel):
    calle: str
    ciudad: str
    codigo_postal: str

class Usuario(BaseModel):
    nombre: str
    direccion: Direccion
    emails: List[str]

# Uso
usuario = Usuario(
    nombre="Ana",
    direccion={
        "calle": "Calle Principal 123",
        "ciudad": "Madrid",
        "codigo_postal": "28001"
    },
    emails=["ana@example.com", "ana.work@example.com"]
)

print(usuario.direccion.ciudad)  # Madrid
```

### 7.6 Config y Alias

```python
from pydantic import BaseModel, Field

class Producto(BaseModel):
    nombre: str = Field(..., alias="productName")  # Alias para JSON
    precio: float = Field(gt=0, description="Precio debe ser positivo")
    stock: int = Field(default=0, ge=0)  # >= 0

    model_config = {
        "str_strip_whitespace": True,  # Eliminar espacios
        "str_min_length": 1,
        "validate_assignment": True,  # Validar en asignación
    }

# Uso con alias
data = {"productName": "Laptop", "precio": 1200}
p = Producto(**data)
print(p.nombre)  # Laptop

# Exportar con alias
print(p.model_dump(by_alias=True))
# {'productName': 'Laptop', 'precio': 1200.0, 'stock': 0}
```

---

## 8. Comparación de Herramientas

### 8.1 Tabla Comparativa

| Característica | Dataclasses | Attrs | Pydantic |
|----------------|-------------|-------|----------|
| Estándar Python | ✅ (3.7+) | ❌ | ❌ |
| Validación | ❌ | ✅ | ✅ |
| Conversión de tipos | ❌ | ✅ | ✅ |
| Serialización JSON | ❌ | ❌ | ✅ |
| Performance | ⚡⚡⚡ | ⚡⚡ | ⚡ |
| Inmutabilidad | ✅ | ✅ | ✅ |
| Herencia | ✅ | ✅ | ✅ |
| Validadores custom | ❌ | ✅ | ✅ |
| Modelos anidados | ⚠️ Manual | ⚠️ Manual | ✅ Auto |
| Uso principal | DTOs simples | Clases de dominio | APIs/Validación |

### 8.2 Cuándo Usar Cada Una

**Dataclasses:**
- Clases de datos simples sin validación
- Cuando no quieres dependencias externas
- Performance es crítica
- Python 3.7+

**Attrs:**
- Necesitas validación pero no serialización JSON
- Quieres más control que dataclasses
- Necesitas conversores automáticos
- Soportas Python < 3.7

**Pydantic:**
- APIs REST (FastAPI)
- Validación de configuración
- Serialización/deserialización JSON
- Modelos de datos complejos con validación
- Integración con bases de datos (SQLAlchemy)

---

## Resumen

En este módulo has aprendido:

✅ **Clases**: Definición, atributos, métodos, encapsulación
✅ **Herencia**: Simple, múltiple, super(), MRO, clases abstractas
✅ **Composición**: "has-a" vs "is-a", cuándo preferir composición
✅ **Dunder Methods**: __str__, __eq__, __add__, __getitem__, etc.
✅ **Dataclasses**: @dataclass, field(), frozen, order
✅ **Attrs**: @attrs.define, validadores, conversores
✅ **Pydantic**: BaseModel, validadores, serialización, modelos anidados

## Recursos Adicionales

- [Python Classes](https://docs.python.org/3/tutorial/classes.html)
- [Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Attrs Documentation](https://www.attrs.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PEP 557 - Data Classes](https://peps.python.org/pep-0557/)

---

**Próximo paso:** Completar el laboratorio con dataclass Order y modelos Pydantic.
