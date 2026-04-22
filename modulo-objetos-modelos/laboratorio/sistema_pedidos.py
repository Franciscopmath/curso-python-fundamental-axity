#!/usr/bin/env python3
"""
Sistema de Gestión de Pedidos - Laboratorio Módulo 4
Objetos y Modelos de Datos

Demuestra:
- Dataclasses con cálculos derivados y comparaciones
- Pydantic para validación y serialización
- Conversión entre modelos Pydantic y entidades de dominio
- Uso práctico de diferentes enfoques para modelado de datos
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

# ============================================================================
# ENUMERACIONES
# ============================================================================


class EstadoPedido(StrEnum):
    """Estados posibles de un pedido."""

    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


class CategoriaProd(StrEnum):
    """Categorías de productos."""

    ELECTRONICA = "electronica"
    ROPA = "ropa"
    ALIMENTOS = "alimentos"
    LIBROS = "libros"
    HOGAR = "hogar"


# ============================================================================
# MODELOS PYDANTIC (CAPA DE API/PRESENTACIÓN)
# ============================================================================


class ItemPedidoIn(BaseModel):
    """Modelo Pydantic para entrada de items de pedido."""

    producto_id: int = Field(gt=0, description="ID del producto")
    nombre: str = Field(min_length=1, max_length=200, description="Nombre del producto")
    precio_unitario: Decimal = Field(gt=0, decimal_places=2, description="Precio por unidad")
    cantidad: int = Field(gt=0, le=1000, description="Cantidad de unidades")
    categoria: CategoriaProd = Field(description="Categoría del producto")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "producto_id": 101,
                "nombre": "Laptop Dell XPS 13",
                "precio_unitario": "1299.99",
                "cantidad": 2,
                "categoria": "electronica",
            }
        }
    )

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        """Valida y normaliza el nombre del producto."""
        nombre_limpio = v.strip()
        if not nombre_limpio:
            raise ValueError("El nombre no puede estar vacío")
        return nombre_limpio

    @field_validator("precio_unitario")
    @classmethod
    def validar_precio(cls, v: Decimal) -> Decimal:
        """Valida que el precio tenga máximo 2 decimales."""
        if v.as_tuple().exponent < -2:
            raise ValueError("El precio no puede tener más de 2 decimales")
        return v


class PedidoIn(BaseModel):
    """Modelo Pydantic para entrada de pedidos."""

    cliente_id: int = Field(gt=0, description="ID del cliente")
    cliente_nombre: str = Field(min_length=1, max_length=200, description="Nombre del cliente")
    items: list[ItemPedidoIn] = Field(min_length=1, description="Lista de items del pedido")
    tasa_impuesto: Decimal = Field(
        ge=0, le=1, decimal_places=4, default=Decimal("0.16"), description="Tasa de impuesto (IVA)"
    )
    descuento_porcentaje: Decimal = Field(
        ge=0, le=100, decimal_places=2, default=Decimal("0"), description="Descuento porcentual"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "cliente_id": 1001,
                "cliente_nombre": "Juan Pérez",
                "items": [
                    {
                        "producto_id": 101,
                        "nombre": "Laptop Dell XPS 13",
                        "precio_unitario": "1299.99",
                        "cantidad": 2,
                        "categoria": "electronica",
                    }
                ],
                "tasa_impuesto": "0.16",
                "descuento_porcentaje": "10.00",
            }
        }
    )

    @field_validator("cliente_nombre")
    @classmethod
    def validar_cliente_nombre(cls, v: str) -> str:
        """Valida y normaliza el nombre del cliente."""
        nombre_limpio = v.strip()
        if not nombre_limpio:
            raise ValueError("El nombre del cliente no puede estar vacío")
        return nombre_limpio

    @field_validator("items")
    @classmethod
    def validar_items_unicos(cls, v: list[ItemPedidoIn]) -> list[ItemPedidoIn]:
        """Valida que no haya productos duplicados."""
        producto_ids = [item.producto_id for item in v]
        if len(producto_ids) != len(set(producto_ids)):
            raise ValueError("No puede haber productos duplicados en el pedido")
        return v


class ItemPedidoOut(BaseModel):
    """Modelo Pydantic para salida de items de pedido."""

    producto_id: int
    nombre: str
    precio_unitario: Decimal
    cantidad: int
    categoria: str
    subtotal: Decimal

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "producto_id": 101,
                "nombre": "Laptop Dell XPS 13",
                "precio_unitario": "1299.99",
                "cantidad": 2,
                "categoria": "electronica",
                "subtotal": "2599.98",
            }
        }
    )


class PedidoOut(BaseModel):
    """Modelo Pydantic para salida de pedidos."""

    pedido_id: int
    cliente_id: int
    cliente_nombre: str
    items: list[ItemPedidoOut]
    subtotal: Decimal
    descuento: Decimal
    subtotal_con_descuento: Decimal
    impuestos: Decimal
    total: Decimal
    estado: str
    fecha_creacion: datetime
    cantidad_items: int
    cantidad_productos: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pedido_id": 5001,
                "cliente_id": 1001,
                "cliente_nombre": "Juan Pérez",
                "items": [
                    {
                        "producto_id": 101,
                        "nombre": "Laptop Dell XPS 13",
                        "precio_unitario": "1299.99",
                        "cantidad": 2,
                        "categoria": "electronica",
                        "subtotal": "2599.98",
                    }
                ],
                "subtotal": "2599.98",
                "descuento": "259.998",
                "subtotal_con_descuento": "2339.982",
                "impuestos": "374.397",
                "total": "2714.379",
                "estado": "pendiente",
                "fecha_creacion": "2026-04-21T10:30:00",
                "cantidad_items": 1,
                "cantidad_productos": 2,
            }
        }
    )


# ============================================================================
# ENTIDADES DE DOMINIO (DATACLASSES)
# ============================================================================


@dataclass(frozen=False, order=False)
class ItemPedido:
    """
    Item individual de un pedido.

    Atributos:
        producto_id: Identificador único del producto
        nombre: Nombre del producto
        precio_unitario: Precio por unidad (Decimal para precisión)
        cantidad: Cantidad de unidades
        categoria: Categoría del producto
    """

    producto_id: int
    nombre: str
    precio_unitario: Decimal
    cantidad: int
    categoria: CategoriaProd

    def __post_init__(self) -> None:
        """Validaciones post-inicialización."""
        if self.producto_id <= 0:
            raise ValueError("producto_id debe ser positivo")
        if not self.nombre or not self.nombre.strip():
            raise ValueError("nombre no puede estar vacío")
        if self.precio_unitario <= 0:
            raise ValueError("precio_unitario debe ser positivo")
        if self.cantidad <= 0:
            raise ValueError("cantidad debe ser positiva")

    @property
    def subtotal(self) -> Decimal:
        """Calcula el subtotal del item (precio × cantidad)."""
        return self.precio_unitario * self.cantidad

    def __str__(self) -> str:
        """Representación legible del item."""
        return (
            f"{self.nombre} (x{self.cantidad}) - "
            f"${self.precio_unitario:.2f} c/u = ${self.subtotal:.2f}"
        )


@dataclass(frozen=False, order=False)
class Pedido:
    """
    Pedido de un cliente con cálculos derivados y comparaciones.

    Demuestra:
    - Uso de properties para cálculos derivados
    - Métodos de comparación personalizados
    - Validaciones en __post_init__
    - Gestión de estado
    """

    cliente_id: int
    cliente_nombre: str
    items: list[ItemPedido]
    tasa_impuesto: Decimal = Decimal("0.16")
    descuento_porcentaje: Decimal = Decimal("0")
    estado: EstadoPedido = EstadoPedido.PENDIENTE
    pedido_id: int = field(default=0, init=False)
    fecha_creacion: datetime = field(default_factory=datetime.now, init=False)

    # Contador de clase para generar IDs únicos
    _contador_id: int = field(default=5000, init=False, repr=False)

    def __post_init__(self) -> None:
        """
        Validaciones y asignación de ID después de la inicialización.
        """
        # Validar cliente
        if self.cliente_id <= 0:
            raise ValueError("cliente_id debe ser positivo")
        if not self.cliente_nombre or not self.cliente_nombre.strip():
            raise ValueError("cliente_nombre no puede estar vacío")

        # Validar items
        if not self.items:
            raise ValueError("El pedido debe tener al menos un item")

        # Validar tasas
        if not (0 <= self.tasa_impuesto <= 1):
            raise ValueError("tasa_impuesto debe estar entre 0 y 1")
        if not (0 <= self.descuento_porcentaje <= 100):
            raise ValueError("descuento_porcentaje debe estar entre 0 y 100")

        # Generar ID único
        Pedido._contador_id += 1
        self.pedido_id = Pedido._contador_id

    # ========================================================================
    # PROPIEDADES CALCULADAS (CÁLCULOS DERIVADOS)
    # ========================================================================

    @property
    def subtotal(self) -> Decimal:
        """Calcula el subtotal sumando todos los items."""
        return sum(item.subtotal for item in self.items)

    @property
    def descuento(self) -> Decimal:
        """Calcula el monto del descuento."""
        return self.subtotal * (self.descuento_porcentaje / 100)

    @property
    def subtotal_con_descuento(self) -> Decimal:
        """Calcula el subtotal después de aplicar descuento."""
        return self.subtotal - self.descuento

    @property
    def impuestos(self) -> Decimal:
        """Calcula los impuestos sobre el subtotal con descuento."""
        return self.subtotal_con_descuento * self.tasa_impuesto

    @property
    def total(self) -> Decimal:
        """Calcula el total final del pedido."""
        return self.subtotal_con_descuento + self.impuestos

    @property
    def cantidad_items(self) -> int:
        """Retorna la cantidad de líneas de items diferentes."""
        return len(self.items)

    @property
    def cantidad_productos(self) -> int:
        """Retorna la cantidad total de productos (suma de cantidades)."""
        return sum(item.cantidad for item in self.items)

    # ========================================================================
    # MÉTODOS DE COMPARACIÓN
    # ========================================================================

    def __eq__(self, other: object) -> bool:
        """
        Compara pedidos por ID.
        Dos pedidos son iguales si tienen el mismo ID.
        """
        if not isinstance(other, Pedido):
            return NotImplemented
        return self.pedido_id == other.pedido_id

    def __lt__(self, other: object) -> bool:
        """
        Compara pedidos por total.
        Permite ordenar pedidos de menor a mayor total.
        """
        if not isinstance(other, Pedido):
            return NotImplemented
        return self.total < other.total

    def __le__(self, other: object) -> bool:
        """Menor o igual comparando por total."""
        if not isinstance(other, Pedido):
            return NotImplemented
        return self.total <= other.total

    def __gt__(self, other: object) -> bool:
        """Mayor comparando por total."""
        if not isinstance(other, Pedido):
            return NotImplemented
        return self.total > other.total

    def __ge__(self, other: object) -> bool:
        """Mayor o igual comparando por total."""
        if not isinstance(other, Pedido):
            return NotImplemented
        return self.total >= other.total

    def __hash__(self) -> int:
        """Hash basado en el ID del pedido."""
        return hash(self.pedido_id)

    # ========================================================================
    # MÉTODOS DE NEGOCIO
    # ========================================================================

    def cambiar_estado(self, nuevo_estado: EstadoPedido) -> None:
        """Cambia el estado del pedido con validación."""
        transiciones_validas = {
            EstadoPedido.PENDIENTE: {EstadoPedido.PROCESANDO, EstadoPedido.CANCELADO},
            EstadoPedido.PROCESANDO: {EstadoPedido.ENVIADO, EstadoPedido.CANCELADO},
            EstadoPedido.ENVIADO: {EstadoPedido.ENTREGADO},
            EstadoPedido.ENTREGADO: set(),
            EstadoPedido.CANCELADO: set(),
        }

        if nuevo_estado not in transiciones_validas.get(self.estado, set()):
            raise ValueError(f"No se puede cambiar de {self.estado.value} a {nuevo_estado.value}")

        self.estado = nuevo_estado

    def agregar_item(self, item: ItemPedido) -> None:
        """Agrega un item al pedido si no existe el producto."""
        if any(i.producto_id == item.producto_id for i in self.items):
            raise ValueError(f"El producto {item.producto_id} ya existe en el pedido")
        self.items.append(item)

    def remover_item(self, producto_id: int) -> None:
        """Remueve un item del pedido por ID de producto."""
        self.items = [i for i in self.items if i.producto_id != producto_id]
        if not self.items:
            raise ValueError("El pedido debe tener al menos un item")

    def aplicar_descuento(self, porcentaje: Decimal) -> None:
        """Aplica un descuento porcentual al pedido."""
        if not (0 <= porcentaje <= 100):
            raise ValueError("El descuento debe estar entre 0 y 100")
        self.descuento_porcentaje = porcentaje

    # ========================================================================
    # REPRESENTACIÓN
    # ========================================================================

    def __str__(self) -> str:
        """Representación legible del pedido."""
        lineas = [
            f"Pedido #{self.pedido_id} - {self.estado.value.upper()}",
            f"Cliente: {self.cliente_nombre} (ID: {self.cliente_id})",
            f"Fecha: {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "Items:",
        ]

        for item in self.items:
            lineas.append(f"  - {item}")

        lineas.extend(
            [
                "",
                f"Subtotal:                ${self.subtotal:.2f}",
                f"Descuento ({self.descuento_porcentaje}%):      -${self.descuento:.2f}",
                f"Subtotal con descuento:  ${self.subtotal_con_descuento:.2f}",
                f"Impuestos ({self.tasa_impuesto * 100}%):       ${self.impuestos:.2f}",
                f"TOTAL:                   ${self.total:.2f}",
            ]
        )

        return "\n".join(lineas)


# ============================================================================
# CONVERSIÓN ENTRE MODELOS PYDANTIC Y ENTIDADES
# ============================================================================


def pydantic_a_item_entidad(item_in: ItemPedidoIn) -> ItemPedido:
    """Convierte un ItemPedidoIn (Pydantic) a ItemPedido (entidad)."""
    return ItemPedido(
        producto_id=item_in.producto_id,
        nombre=item_in.nombre,
        precio_unitario=item_in.precio_unitario,
        cantidad=item_in.cantidad,
        categoria=item_in.categoria,
    )


def pydantic_a_pedido_entidad(pedido_in: PedidoIn) -> Pedido:
    """Convierte un PedidoIn (Pydantic) a Pedido (entidad)."""
    items_entidad = [pydantic_a_item_entidad(item) for item in pedido_in.items]

    return Pedido(
        cliente_id=pedido_in.cliente_id,
        cliente_nombre=pedido_in.cliente_nombre,
        items=items_entidad,
        tasa_impuesto=pedido_in.tasa_impuesto,
        descuento_porcentaje=pedido_in.descuento_porcentaje,
    )


def item_entidad_a_pydantic(item: ItemPedido) -> ItemPedidoOut:
    """Convierte un ItemPedido (entidad) a ItemPedidoOut (Pydantic)."""
    return ItemPedidoOut(
        producto_id=item.producto_id,
        nombre=item.nombre,
        precio_unitario=item.precio_unitario,
        cantidad=item.cantidad,
        categoria=item.categoria.value,
        subtotal=item.subtotal,
    )


def pedido_entidad_a_pydantic(pedido: Pedido) -> PedidoOut:
    """Convierte un Pedido (entidad) a PedidoOut (Pydantic)."""
    items_out = [item_entidad_a_pydantic(item) for item in pedido.items]

    return PedidoOut(
        pedido_id=pedido.pedido_id,
        cliente_id=pedido.cliente_id,
        cliente_nombre=pedido.cliente_nombre,
        items=items_out,
        subtotal=pedido.subtotal,
        descuento=pedido.descuento,
        subtotal_con_descuento=pedido.subtotal_con_descuento,
        impuestos=pedido.impuestos,
        total=pedido.total,
        estado=pedido.estado.value,
        fecha_creacion=pedido.fecha_creacion,
        cantidad_items=pedido.cantidad_items,
        cantidad_productos=pedido.cantidad_productos,
    )


# ============================================================================
# FUNCIONES DE DEMOSTRACIÓN
# ============================================================================


def ejemplo_basico() -> None:
    """Ejemplo básico de creación y uso de pedidos."""
    print("=" * 80)
    print("EJEMPLO 1: Creación Básica de Pedido")
    print("=" * 80)

    # Crear items
    item1 = ItemPedido(
        producto_id=101,
        nombre="Laptop Dell XPS 13",
        precio_unitario=Decimal("1299.99"),
        cantidad=2,
        categoria=CategoriaProd.ELECTRONICA,
    )

    item2 = ItemPedido(
        producto_id=202,
        nombre="Mouse Logitech MX Master 3",
        precio_unitario=Decimal("99.99"),
        cantidad=3,
        categoria=CategoriaProd.ELECTRONICA,
    )

    # Crear pedido
    pedido = Pedido(
        cliente_id=1001,
        cliente_nombre="Juan Pérez",
        items=[item1, item2],
        descuento_porcentaje=Decimal("10"),
    )

    print(pedido)
    print("\n")


def ejemplo_calculos_derivados() -> None:
    """Demuestra el uso de propiedades calculadas."""
    print("=" * 80)
    print("EJEMPLO 2: Cálculos Derivados con Properties")
    print("=" * 80)

    item = ItemPedido(
        producto_id=303,
        nombre="Libro Python Avanzado",
        precio_unitario=Decimal("45.50"),
        cantidad=5,
        categoria=CategoriaProd.LIBROS,
    )

    pedido = Pedido(
        cliente_id=1002,
        cliente_nombre="María García",
        items=[item],
        tasa_impuesto=Decimal("0.16"),
        descuento_porcentaje=Decimal("15"),
    )

    print(f"Cliente: {pedido.cliente_nombre}")
    print(f"Pedido ID: {pedido.pedido_id}")
    print()
    print("Cálculos automáticos:")
    print(f"  Subtotal:                ${pedido.subtotal:.2f}")
    print(f"  Descuento (15%):         -${pedido.descuento:.2f}")
    print(f"  Subtotal con descuento:  ${pedido.subtotal_con_descuento:.2f}")
    print(f"  Impuestos (16%):         ${pedido.impuestos:.2f}")
    print(f"  TOTAL:                   ${pedido.total:.2f}")
    print()
    print(f"Cantidad de líneas:  {pedido.cantidad_items}")
    print(f"Cantidad de productos: {pedido.cantidad_productos}")
    print("\n")


def ejemplo_comparaciones() -> None:
    """Demuestra las comparaciones entre pedidos."""
    print("=" * 80)
    print("EJEMPLO 3: Comparaciones entre Pedidos")
    print("=" * 80)

    pedidos = [
        Pedido(
            cliente_id=1003,
            cliente_nombre="Carlos López",
            items=[
                ItemPedido(
                    producto_id=401,
                    nombre="Teclado Mecánico",
                    precio_unitario=Decimal("150.00"),
                    cantidad=1,
                    categoria=CategoriaProd.ELECTRONICA,
                )
            ],
        ),
        Pedido(
            cliente_id=1004,
            cliente_nombre="Ana Martínez",
            items=[
                ItemPedido(
                    producto_id=501,
                    nombre="Monitor 4K",
                    precio_unitario=Decimal("450.00"),
                    cantidad=2,
                    categoria=CategoriaProd.ELECTRONICA,
                )
            ],
        ),
        Pedido(
            cliente_id=1005,
            cliente_nombre="Luis Rodríguez",
            items=[
                ItemPedido(
                    producto_id=601,
                    nombre="Silla Ergonómica",
                    precio_unitario=Decimal("299.99"),
                    cantidad=1,
                    categoria=CategoriaProd.HOGAR,
                )
            ],
        ),
    ]

    print("Pedidos creados:")
    for p in pedidos:
        print(f"  Pedido #{p.pedido_id} - {p.cliente_nombre}: ${p.total:.2f}")

    print("\nComparaciones:")
    print(f"  Pedido #1 < Pedido #2: {pedidos[0] < pedidos[1]}")
    print(f"  Pedido #2 > Pedido #3: {pedidos[1] > pedidos[2]}")
    print(f"  Pedido #1 == Pedido #1: {pedidos[0] == pedidos[0]}")

    print("\nOrdenados por total (menor a mayor):")
    for p in sorted(pedidos):
        print(f"  Pedido #{p.pedido_id} - ${p.total:.2f}")

    print("\nOrdenados por total (mayor a menor):")
    for p in sorted(pedidos, reverse=True):
        print(f"  Pedido #{p.pedido_id} - ${p.total:.2f}")

    print("\n")


def ejemplo_gestion_estado() -> None:
    """Demuestra la gestión de estado del pedido."""
    print("=" * 80)
    print("EJEMPLO 4: Gestión de Estado del Pedido")
    print("=" * 80)

    pedido = Pedido(
        cliente_id=1006,
        cliente_nombre="Patricia Sánchez",
        items=[
            ItemPedido(
                producto_id=701,
                nombre="Audífonos Sony WH-1000XM5",
                precio_unitario=Decimal("349.99"),
                cantidad=1,
                categoria=CategoriaProd.ELECTRONICA,
            )
        ],
    )

    print(f"Estado inicial: {pedido.estado.value}")

    # Transición válida
    pedido.cambiar_estado(EstadoPedido.PROCESANDO)
    print(f"Estado después de procesamiento: {pedido.estado.value}")

    pedido.cambiar_estado(EstadoPedido.ENVIADO)
    print(f"Estado después de envío: {pedido.estado.value}")

    pedido.cambiar_estado(EstadoPedido.ENTREGADO)
    print(f"Estado final: {pedido.estado.value}")

    # Intentar transición inválida
    print("\nIntentando transición inválida (entregado -> procesando)...")
    try:
        pedido.cambiar_estado(EstadoPedido.PROCESANDO)
    except ValueError as e:
        print(f"  Error esperado: {e}")

    print("\n")


def ejemplo_pydantic_validacion() -> None:
    """Demuestra validación con Pydantic."""
    print("=" * 80)
    print("EJEMPLO 5: Validación con Pydantic")
    print("=" * 80)

    # Caso válido
    print("Caso 1: Entrada válida")
    pedido_in = PedidoIn(
        cliente_id=2001,
        cliente_nombre="Roberto Fernández",
        items=[
            ItemPedidoIn(
                producto_id=801,
                nombre="  Tablet Samsung Galaxy Tab S9  ",  # Nombre con espacios
                precio_unitario=Decimal("599.99"),
                cantidad=1,
                categoria=CategoriaProd.ELECTRONICA,
            )
        ],
        descuento_porcentaje=Decimal("5.00"),
    )
    print(f"  ✓ Pedido válido para cliente: {pedido_in.cliente_nombre}")
    print(f"  ✓ Nombre normalizado: '{pedido_in.items[0].nombre}'")

    # Caso inválido: precio negativo
    print("\nCaso 2: Precio inválido (negativo)")
    try:
        ItemPedidoIn(
            producto_id=802,
            nombre="Producto Inválido",
            precio_unitario=Decimal("-10.00"),
            cantidad=1,
            categoria=CategoriaProd.ELECTRONICA,
        )
    except Exception as e:
        print(f"  ✗ Error esperado: {e}")

    # Caso inválido: cantidad excesiva
    print("\nCaso 3: Cantidad inválida (excede límite)")
    try:
        ItemPedidoIn(
            producto_id=803,
            nombre="Producto con mucha cantidad",
            precio_unitario=Decimal("10.00"),
            cantidad=2000,
            categoria=CategoriaProd.ELECTRONICA,
        )
    except Exception as e:
        print(f"  ✗ Error esperado: {e}")

    # Caso inválido: productos duplicados
    print("\nCaso 4: Productos duplicados")
    try:
        PedidoIn(
            cliente_id=2002,
            cliente_nombre="Cliente Test",
            items=[
                ItemPedidoIn(
                    producto_id=900,
                    nombre="Producto A",
                    precio_unitario=Decimal("100"),
                    cantidad=1,
                    categoria=CategoriaProd.ELECTRONICA,
                ),
                ItemPedidoIn(
                    producto_id=900,  # ID duplicado
                    nombre="Producto B",
                    precio_unitario=Decimal("200"),
                    cantidad=1,
                    categoria=CategoriaProd.ELECTRONICA,
                ),
            ],
        )
    except Exception as e:
        print(f"  ✗ Error esperado: {e}")

    print("\n")


def ejemplo_conversion_modelos() -> None:
    """Demuestra la conversión entre modelos Pydantic y entidades."""
    print("=" * 80)
    print("EJEMPLO 6: Conversión Pydantic ↔ Entidad")
    print("=" * 80)

    # Crear pedido con Pydantic (simula entrada de API)
    print("1. Crear pedido desde API (Pydantic):")
    pedido_in = PedidoIn(
        cliente_id=3001,
        cliente_nombre="Elena Torres",
        items=[
            ItemPedidoIn(
                producto_id=1001,
                nombre="Cámara Canon EOS R5",
                precio_unitario=Decimal("3899.00"),
                cantidad=1,
                categoria=CategoriaProd.ELECTRONICA,
            ),
            ItemPedidoIn(
                producto_id=1002,
                nombre="Lente Canon RF 24-70mm",
                precio_unitario=Decimal("1099.00"),
                cantidad=1,
                categoria=CategoriaProd.ELECTRONICA,
            ),
        ],
        tasa_impuesto=Decimal("0.16"),
        descuento_porcentaje=Decimal("12.50"),
    )
    print(f"  ✓ PedidoIn creado: {pedido_in.cliente_nombre}")
    print(f"  ✓ Items: {len(pedido_in.items)}")

    # Convertir a entidad de dominio
    print("\n2. Convertir a entidad de dominio:")
    pedido_entidad = pydantic_a_pedido_entidad(pedido_in)
    print(f"  ✓ Pedido entidad creado: #{pedido_entidad.pedido_id}")
    print(f"  ✓ Total calculado: ${pedido_entidad.total:.2f}")

    # Procesar en lógica de negocio
    print("\n3. Procesar en lógica de negocio:")
    pedido_entidad.cambiar_estado(EstadoPedido.PROCESANDO)
    print(f"  ✓ Estado cambiado a: {pedido_entidad.estado.value}")

    # Convertir a modelo de salida
    print("\n4. Convertir a modelo de salida (API response):")
    pedido_out = pedido_entidad_a_pydantic(pedido_entidad)
    print("  ✓ PedidoOut generado")
    print("  ✓ JSON serializable")

    # Mostrar JSON
    print("\n5. Serialización a JSON:")
    json_data = pedido_out.model_dump_json(indent=2)
    print(json_data)

    print("\n")


def ejemplo_uso_conjunto() -> None:
    """Ejemplo completo mostrando el flujo completo."""
    print("=" * 80)
    print("EJEMPLO 7: Flujo Completo de Procesamiento")
    print("=" * 80)

    # 1. Datos de entrada (simula request de API)
    print("1. ENTRADA: Datos del cliente (API Request)")
    datos_entrada: dict[str, Any] = {
        "cliente_id": 4001,
        "cliente_nombre": "Empresa Tech Solutions",
        "items": [
            {
                "producto_id": 2001,
                "nombre": "Servidor Dell PowerEdge",
                "precio_unitario": "4999.99",
                "cantidad": 2,
                "categoria": "electronica",
            },
            {
                "producto_id": 2002,
                "nombre": "Switch Cisco 48 puertos",
                "precio_unitario": "1299.99",
                "cantidad": 3,
                "categoria": "electronica",
            },
            {
                "producto_id": 2003,
                "nombre": "UPS APC 3000VA",
                "precio_unitario": "899.99",
                "cantidad": 2,
                "categoria": "electronica",
            },
        ],
        "tasa_impuesto": "0.16",
        "descuento_porcentaje": "8.00",
    }
    print(f"  Cliente: {datos_entrada['cliente_nombre']}")
    print(f"  Items: {len(datos_entrada['items'])}")

    # 2. Validar con Pydantic
    print("\n2. VALIDACIÓN: Validar y parsear con Pydantic")
    pedido_in = PedidoIn.model_validate(datos_entrada)
    print("  ✓ Datos validados correctamente")

    # 3. Convertir a entidad de dominio
    print("\n3. CONVERSIÓN: Crear entidad de dominio")
    pedido = pydantic_a_pedido_entidad(pedido_in)
    print(f"  ✓ Pedido #{pedido.pedido_id} creado")

    # 4. Aplicar lógica de negocio
    print("\n4. LÓGICA DE NEGOCIO: Procesar pedido")
    pedido.cambiar_estado(EstadoPedido.PROCESANDO)
    print(f"  ✓ Estado: {pedido.estado.value}")
    print(f"  ✓ Total: ${pedido.total:.2f}")

    # 5. Preparar respuesta
    print("\n5. SALIDA: Preparar respuesta (API Response)")
    pedido_out = pedido_entidad_a_pydantic(pedido)
    print("  ✓ Modelo de salida generado")

    # 6. Mostrar resumen
    print("\n6. RESUMEN DEL PEDIDO:")
    print(f"  ID: {pedido_out.pedido_id}")
    print(f"  Cliente: {pedido_out.cliente_nombre}")
    print(f"  Items: {pedido_out.cantidad_items} líneas, {pedido_out.cantidad_productos} productos")
    print(f"  Subtotal: ${pedido_out.subtotal:.2f}")
    print(f"  Descuento: -${pedido_out.descuento:.2f}")
    print(f"  Impuestos: ${pedido_out.impuestos:.2f}")
    print(f"  TOTAL: ${pedido_out.total:.2f}")
    print(f"  Estado: {pedido_out.estado}")

    print("\n")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================


def main() -> None:
    """Ejecuta todos los ejemplos de demostración."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "SISTEMA DE GESTIÓN DE PEDIDOS" + " " * 34 + "║")
    print("║" + " " * 12 + "Objetos y Modelos de Datos - Módulo 4" + " " * 29 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    ejemplos = [
        ejemplo_basico,
        ejemplo_calculos_derivados,
        ejemplo_comparaciones,
        ejemplo_gestion_estado,
        ejemplo_pydantic_validacion,
        ejemplo_conversion_modelos,
        ejemplo_uso_conjunto,
    ]

    for ejemplo in ejemplos:
        ejemplo()

    print("=" * 80)
    print("FIN DE EJEMPLOS")
    print("=" * 80)
    print("""
Conceptos demostrados:
  ✓ Dataclasses con propiedades calculadas
  ✓ Métodos de comparación personalizados (__lt__, __eq__, etc.)
  ✓ Validación en __post_init__
  ✓ Pydantic para validación de entrada/salida
  ✓ Conversión entre modelos Pydantic y entidades
  ✓ Gestión de estado con validación de transiciones
  ✓ Uso de Decimal para precisión monetaria
  ✓ Enumeraciones (Enum) para valores constantes
  ✓ Type hints completos
  ✓ Documentación con docstrings
""")


if __name__ == "__main__":
    main()
