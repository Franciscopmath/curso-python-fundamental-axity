# Laboratorio: Sistema de Gestión de Pedidos

Sistema completo de gestión de pedidos que demuestra el uso de dataclasses, Pydantic y conversión entre modelos.

## Objetivos

Este laboratorio implementa:

1. **Dataclasses con cálculos derivados**: Clase `Pedido` con properties para cálculos automáticos
2. **Métodos de comparación**: Implementación de `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`
3. **Validación con Pydantic**: Modelos `PedidoIn` y `PedidoOut` con validaciones robustas
4. **Conversión de modelos**: Funciones bidireccionales entre Pydantic y entidades de dominio
5. **Gestión de estado**: Máquina de estados para el flujo del pedido
6. **Precisión monetaria**: Uso de `Decimal` para cálculos financieros

## Estructura del Código

```
sistema_pedidos.py
├── Enumeraciones
│   ├── EstadoPedido
│   └── CategoriaProd
├── Modelos Pydantic (Capa API)
│   ├── ItemPedidoIn
│   ├── PedidoIn
│   ├── ItemPedidoOut
│   └── PedidoOut
├── Entidades de Dominio (Dataclasses)
│   ├── ItemPedido
│   └── Pedido
├── Funciones de Conversión
│   ├── pydantic_a_item_entidad()
│   ├── pydantic_a_pedido_entidad()
│   ├── item_entidad_a_pydantic()
│   └── pedido_entidad_a_pydantic()
└── Ejemplos de Uso
    ├── ejemplo_basico()
    ├── ejemplo_calculos_derivados()
    ├── ejemplo_comparaciones()
    ├── ejemplo_gestion_estado()
    ├── ejemplo_pydantic_validacion()
    ├── ejemplo_conversion_modelos()
    └── ejemplo_uso_conjunto()
```

## Instalación

### 1. Instalar dependencias

```bash
cd modulo-objetos-modelos/laboratorio
poetry install
```

Esto instalará:
- **pydantic** >= 2.10.6: Para validación y serialización
- **black**, **isort**, **ruff**: Herramientas de calidad
- **pytest**: Para testing

### 2. Activar el entorno virtual

```bash
poetry shell
```

## Uso

### Ejecutar todos los ejemplos

```bash
python sistema_pedidos.py
```

Esto ejecutará 7 ejemplos completos que demuestran:

1. **Creación básica**: Crear pedidos con items
2. **Cálculos derivados**: Properties para subtotal, descuento, impuestos, total
3. **Comparaciones**: Ordenar pedidos por total
4. **Gestión de estado**: Transiciones válidas e inválidas
5. **Validación Pydantic**: Casos válidos e inválidos
6. **Conversión de modelos**: Pydantic ↔ Entidad
7. **Flujo completo**: Desde API request hasta API response

### Usar como módulo

```python
from sistema_pedidos import (
    Pedido,
    ItemPedido,
    PedidoIn,
    PedidoOut,
    pydantic_a_pedido_entidad,
    pedido_entidad_a_pydantic,
)
from decimal import Decimal

# Crear pedido desde datos de API
datos_api = {
    "cliente_id": 1001,
    "cliente_nombre": "Juan Pérez",
    "items": [
        {
            "producto_id": 101,
            "nombre": "Laptop",
            "precio_unitario": "1299.99",
            "cantidad": 1,
            "categoria": "electronica",
        }
    ],
}

# Validar con Pydantic
pedido_in = PedidoIn.model_validate(datos_api)

# Convertir a entidad de dominio
pedido = pydantic_a_pedido_entidad(pedido_in)

# Usar propiedades calculadas
print(f"Total: ${pedido.total:.2f}")

# Convertir a modelo de salida
pedido_out = pedido_entidad_a_pydantic(pedido)
json_response = pedido_out.model_dump_json()
```

## Conceptos Implementados

### 1. Dataclass con Propiedades Calculadas

La clase `Pedido` demuestra cómo usar `@property` para cálculos derivados:

```python
@property
def total(self) -> Decimal:
    """Calcula el total final del pedido."""
    return self.subtotal_con_descuento + self.impuestos
```

**Ventajas:**
- Los cálculos se ejecutan automáticamente
- No es necesario sincronizar valores manualmente
- El código es más mantenible y menos propenso a errores

### 2. Métodos de Comparación

Implementa `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__` para:

```python
# Comparar por ID
pedido1 == pedido2  # Compara pedido_id

# Ordenar por total
sorted(pedidos)  # Ordena de menor a mayor total
max(pedidos)     # Pedido con mayor total
min(pedidos)     # Pedido con menor total
```

### 3. Validación con `__post_init__`

Validaciones en dataclasses después de la inicialización:

```python
def __post_init__(self) -> None:
    if self.cliente_id <= 0:
        raise ValueError("cliente_id debe ser positivo")
    if not self.items:
        raise ValueError("El pedido debe tener al menos un item")
```

### 4. Pydantic para Validación de API

Los modelos Pydantic validan datos de entrada/salida:

```python
class PedidoIn(BaseModel):
    cliente_id: int = Field(gt=0)
    items: list[ItemPedidoIn] = Field(min_length=1)

    @field_validator("items")
    @classmethod
    def validar_items_unicos(cls, v):
        # Validación personalizada
        ...
```

**Ventajas:**
- Validación automática de tipos
- Mensajes de error descriptivos
- Serialización/deserialización JSON
- Documentación automática (OpenAPI)

### 5. Separación de Responsabilidades

El código demuestra arquitectura en capas:

- **Pydantic (Capa de API)**: Validación de entrada/salida
- **Dataclasses (Capa de Dominio)**: Lógica de negocio
- **Funciones de Conversión**: Traducción entre capas

### 6. Gestión de Estado

Máquina de estados con transiciones válidas:

```python
PENDIENTE → PROCESANDO → ENVIADO → ENTREGADO
         ↓            ↓
      CANCELADO   CANCELADO
```

### 7. Uso de Decimal

Para cálculos monetarios precisos:

```python
from decimal import Decimal

precio = Decimal("1299.99")  # Precisión exacta
total = precio * cantidad     # Sin errores de redondeo
```

**Por qué no usar float:**
```python
# INCORRECTO con float
0.1 + 0.2  # 0.30000000000000004

# CORRECTO con Decimal
Decimal("0.1") + Decimal("0.2")  # 0.3
```

## Ejemplos de Salida

### Ejemplo 1: Creación Básica

```
Pedido #5001 - PENDIENTE
Cliente: Juan Pérez (ID: 1001)
Fecha: 2026-04-21 10:30:00

Items:
  - Laptop Dell XPS 13 (x2) - $1299.99 c/u = $2599.98
  - Mouse Logitech MX Master 3 (x3) - $99.99 c/u = $299.97

Subtotal:                $2899.95
Descuento (10%):         -$289.995
Subtotal con descuento:  $2609.955
Impuestos (16.0%):       $417.593
TOTAL:                   $3027.548
```

### Ejemplo 2: Validación Pydantic

```
Caso 1: Entrada válida
  ✓ Pedido válido para cliente: Roberto Fernández
  ✓ Nombre normalizado: 'Tablet Samsung Galaxy Tab S9'

Caso 2: Precio inválido (negativo)
  ✗ Error: Input should be greater than 0

Caso 3: Cantidad inválida (excede límite)
  ✗ Error: Input should be less than or equal to 1000
```

### Ejemplo 3: Comparaciones

```
Pedidos creados:
  Pedido #5001 - Carlos López: $174.00
  Pedido #5002 - Ana Martínez: $1044.00
  Pedido #5003 - Luis Rodríguez: $347.99

Comparaciones:
  Pedido #1 < Pedido #2: True
  Pedido #2 > Pedido #3: True

Ordenados por total (menor a mayor):
  Pedido #5001 - $174.00
  Pedido #5003 - $347.99
  Pedido #5002 - $1044.00
```

## Verificación de Calidad

### Ejecutar linter

```bash
poetry run ruff check sistema_pedidos.py
```

### Formatear código

```bash
poetry run black sistema_pedidos.py
poetry run isort sistema_pedidos.py
```

### Ejecutar todas las herramientas

```bash
poetry run ruff check --fix sistema_pedidos.py && \
poetry run isort sistema_pedidos.py && \
poetry run black sistema_pedidos.py
```

## Ejercicios Propuestos

### Ejercicio 1: Agregar método de descuento
Implementa un método `aplicar_descuento_categoria()` que aplique descuento solo a items de cierta categoría.

### Ejercicio 2: Historial de estados
Agrega un campo `historial_estados` que registre todas las transiciones de estado con timestamps.

### Ejercicio 3: Validación de stock
Extiende `ItemPedido` para verificar disponibilidad en inventario antes de crear el pedido.

### Ejercicio 4: Serialización personalizada
Implementa un método que exporte el pedido a formato CSV.

### Ejercicio 5: Tests unitarios
Crea tests con pytest para validar:
- Cálculos de totales
- Transiciones de estado
- Validaciones de Pydantic
- Comparaciones entre pedidos

## Puntos Clave

1. **Dataclasses**: Ideales para entidades de dominio con lógica de negocio
2. **Pydantic**: Perfecto para validación de datos externos (API, archivos)
3. **Properties**: Cálculos derivados sin duplicar datos
4. **Decimal**: Obligatorio para cálculos monetarios
5. **Type hints**: Mejoran legibilidad y detectan errores
6. **Validación**: Múltiples capas (Pydantic + `__post_init__`)
7. **Separación de capas**: API (Pydantic) ↔ Dominio (Dataclasses)

## Recursos Adicionales

- [Documentación de dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Documentación de Pydantic](https://docs.pydantic.dev/)
- [PEP 557 - Data Classes](https://peps.python.org/pep-0557/)
- [Decimal - Aritmética de punto fijo](https://docs.python.org/3/library/decimal.html)

## Notas

- El código usa Python 3.12 con type hints modernos
- Cumple 100% con PEP 8
- Incluye 600+ líneas de código documentado
- 7 ejemplos ejecutables que demuestran todos los conceptos
- Listo para extender con tests unitarios y más funcionalidades
