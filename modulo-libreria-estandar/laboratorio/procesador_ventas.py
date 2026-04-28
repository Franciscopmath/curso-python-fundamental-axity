#!/usr/bin/env python3
"""
Procesador de Ventas - Laboratorio Módulo 6
Librería Estándar y E/S

Demuestra:
- pathlib para manejo de rutas
- CSV para lectura de datos
- JSON para exportación
- datetime para procesamiento de fechas
- logging con diferentes niveles
- Cálculo de métricas y estadísticas
"""

import csv
import json
import logging
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================


def configurar_logging(nivel: str = "INFO", archivo_log: Path | None = None) -> logging.Logger:
    """
    Configura el sistema de logging con diferentes niveles y handlers.

    Args:
        nivel: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        archivo_log: Ruta opcional para guardar logs en archivo

    Returns:
        Logger configurado
    """
    logger = logging.getLogger("procesador_ventas")
    logger.setLevel(getattr(logging, nivel.upper()))

    # Eliminar handlers existentes
    logger.handlers.clear()

    # Formato detallado
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para archivo (si se especifica)
    if archivo_log:
        archivo_log.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            archivo_log,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Logger global
logger = configurar_logging()


# ============================================================================
# MODELOS DE DATOS
# ============================================================================


@dataclass
class Venta:
    """Representa una venta individual."""

    fecha: datetime
    producto: str
    categoria: str
    cantidad: int
    precio_unitario: Decimal
    vendedor: str
    region: str
    id_venta: str = field(default="")

    def __post_init__(self) -> None:
        """Validaciones después de la inicialización."""
        if self.cantidad <= 0:
            raise ValueError(f"Cantidad inválida: {self.cantidad}")
        if self.precio_unitario <= 0:
            raise ValueError(f"Precio inválido: {self.precio_unitario}")

        if not self.id_venta:
            self.id_venta = f"{self.fecha.strftime('%Y%m%d')}-{self.producto[:3].upper()}"

    @property
    def total(self) -> Decimal:
        """Calcula el total de la venta."""
        return Decimal(self.cantidad) * self.precio_unitario

    @property
    def mes(self) -> int:
        """Retorna el mes de la venta."""
        return self.fecha.month

    @property
    def trimestre(self) -> int:
        """Retorna el trimestre de la venta (1-4)."""
        return (self.fecha.month - 1) // 3 + 1

    def to_dict(self) -> dict[str, Any]:
        """Convierte la venta a diccionario para JSON."""
        return {
            "id_venta": self.id_venta,
            "fecha": self.fecha.isoformat(),
            "producto": self.producto,
            "categoria": self.categoria,
            "cantidad": self.cantidad,
            "precio_unitario": float(self.precio_unitario),
            "total": float(self.total),
            "vendedor": self.vendedor,
            "region": self.region,
            "mes": self.mes,
            "trimestre": self.trimestre,
        }


@dataclass
class MetricasVentas:
    """Métricas agregadas de ventas."""

    total_ventas: Decimal
    cantidad_transacciones: int
    ticket_promedio: Decimal
    venta_minima: Decimal
    venta_maxima: Decimal
    productos_vendidos: int
    periodo_inicio: datetime
    periodo_fin: datetime
    ventas_por_categoria: dict[str, Decimal] = field(default_factory=dict)
    ventas_por_region: dict[str, Decimal] = field(default_factory=dict)
    ventas_por_mes: dict[int, Decimal] = field(default_factory=dict)
    top_productos: list[tuple[str, Decimal]] = field(default_factory=list)
    top_vendedores: list[tuple[str, Decimal]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convierte métricas a diccionario para JSON."""
        return {
            "resumen": {
                "total_ventas": float(self.total_ventas),
                "cantidad_transacciones": self.cantidad_transacciones,
                "ticket_promedio": float(self.ticket_promedio),
                "venta_minima": float(self.venta_minima),
                "venta_maxima": float(self.venta_maxima),
                "productos_vendidos": self.productos_vendidos,
            },
            "periodo": {
                "inicio": self.periodo_inicio.isoformat(),
                "fin": self.periodo_fin.isoformat(),
                "dias": (self.periodo_fin - self.periodo_inicio).days + 1,
            },
            "por_categoria": {k: float(v) for k, v in self.ventas_por_categoria.items()},
            "por_region": {k: float(v) for k, v in self.ventas_por_region.items()},
            "por_mes": {str(k): float(v) for k, v in self.ventas_por_mes.items()},
            "top_productos": [
                {"producto": prod, "ventas": float(total)} for prod, total in self.top_productos
            ],
            "top_vendedores": [
                {"vendedor": vend, "ventas": float(total)} for vend, total in self.top_vendedores
            ],
        }


# ============================================================================
# FUNCIONES DE PROCESAMIENTO
# ============================================================================


def leer_csv_ventas(archivo_csv: Path) -> list[Venta]:
    """
    Lee archivo CSV de ventas y retorna lista de objetos Venta.

    Args:
        archivo_csv: Ruta al archivo CSV

    Returns:
        Lista de objetos Venta

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si hay errores en los datos
    """
    logger.info("Leyendo archivo CSV: %s", archivo_csv)

    if not archivo_csv.exists():
        logger.error("Archivo no encontrado: %s", archivo_csv)
        raise FileNotFoundError(f"Archivo no encontrado: {archivo_csv}")

    ventas: list[Venta] = []
    errores = 0

    try:
        with archivo_csv.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for num_linea, fila in enumerate(reader, start=2):  # 2 porque línea 1 es encabezado
                try:
                    # Parsear fecha
                    fecha = datetime.strptime(fila["fecha"], "%Y-%m-%d")

                    # Parsear precio con Decimal para precisión
                    precio = Decimal(fila["precio_unitario"])

                    # Crear objeto Venta
                    venta = Venta(
                        fecha=fecha,
                        producto=fila["producto"].strip(),
                        categoria=fila["categoria"].strip(),
                        cantidad=int(fila["cantidad"]),
                        precio_unitario=precio,
                        vendedor=fila["vendedor"].strip(),
                        region=fila["region"].strip(),
                    )

                    ventas.append(venta)
                    logger.debug(
                        "Venta procesada: %s - %s (Total: $%.2f)",
                        venta.id_venta,
                        venta.producto,
                        venta.total,
                    )

                except (ValueError, KeyError) as e:
                    errores += 1
                    logger.warning("Error en línea %d: %s - Fila: %s", num_linea, e, fila)
                    continue

    except Exception as e:
        logger.error("Error al leer archivo CSV: %s", e)
        raise

    logger.info("CSV procesado: %d ventas exitosas, %d errores", len(ventas), errores)

    if errores > 0:
        logger.warning("Se encontraron %d filas con errores que fueron omitidas", errores)

    return ventas


def calcular_metricas(ventas: list[Venta]) -> MetricasVentas:
    """
    Calcula métricas y estadísticas de las ventas.

    Args:
        ventas: Lista de objetos Venta

    Returns:
        Objeto MetricasVentas con estadísticas calculadas
    """
    logger.info("Calculando métricas de %d ventas", len(ventas))

    if not ventas:
        logger.warning("No hay ventas para procesar")
        raise ValueError("No hay ventas para calcular métricas")

    # Métricas básicas
    totales = [v.total for v in ventas]
    total_ventas = sum(totales)
    cantidad_transacciones = len(ventas)
    ticket_promedio = total_ventas / Decimal(cantidad_transacciones)
    venta_minima = min(totales)
    venta_maxima = max(totales)

    # Productos únicos
    productos_unicos = len({v.producto for v in ventas})

    # Periodo
    fechas = [v.fecha for v in ventas]
    periodo_inicio = min(fechas)
    periodo_fin = max(fechas)

    logger.debug("Total ventas: $%.2f", total_ventas)
    logger.debug("Ticket promedio: $%.2f", ticket_promedio)

    # Ventas por categoría
    ventas_por_categoria: dict[str, Decimal] = defaultdict(Decimal)
    for venta in ventas:
        ventas_por_categoria[venta.categoria] += venta.total

    logger.debug("Categorías procesadas: %d", len(ventas_por_categoria))

    # Ventas por región
    ventas_por_region: dict[str, Decimal] = defaultdict(Decimal)
    for venta in ventas:
        ventas_por_region[venta.region] += venta.total

    logger.debug("Regiones procesadas: %d", len(ventas_por_region))

    # Ventas por mes
    ventas_por_mes: dict[int, Decimal] = defaultdict(Decimal)
    for venta in ventas:
        ventas_por_mes[venta.mes] += venta.total

    # Top productos
    ventas_por_producto: dict[str, Decimal] = defaultdict(Decimal)
    for venta in ventas:
        ventas_por_producto[venta.producto] += venta.total

    top_productos = sorted(ventas_por_producto.items(), key=lambda x: x[1], reverse=True)[:10]

    logger.debug("Top producto: %s con $%.2f", top_productos[0][0], top_productos[0][1])

    # Top vendedores
    ventas_por_vendedor: dict[str, Decimal] = defaultdict(Decimal)
    for venta in ventas:
        ventas_por_vendedor[venta.vendedor] += venta.total

    top_vendedores = sorted(ventas_por_vendedor.items(), key=lambda x: x[1], reverse=True)[:10]

    logger.info("Métricas calculadas exitosamente")

    return MetricasVentas(
        total_ventas=total_ventas,
        cantidad_transacciones=cantidad_transacciones,
        ticket_promedio=ticket_promedio,
        venta_minima=venta_minima,
        venta_maxima=venta_maxima,
        productos_vendidos=productos_unicos,
        periodo_inicio=periodo_inicio,
        periodo_fin=periodo_fin,
        ventas_por_categoria=dict(ventas_por_categoria),
        ventas_por_region=dict(ventas_por_region),
        ventas_por_mes=dict(ventas_por_mes),
        top_productos=top_productos,
        top_vendedores=top_vendedores,
    )


def filtrar_ventas(
    ventas: list[Venta],
    categoria: str | None = None,
    region: str | None = None,
    fecha_inicio: datetime | None = None,
    fecha_fin: datetime | None = None,
) -> list[Venta]:
    """
    Filtra ventas según criterios.

    Args:
        ventas: Lista de ventas
        categoria: Filtrar por categoría
        region: Filtrar por región
        fecha_inicio: Fecha de inicio del rango
        fecha_fin: Fecha de fin del rango

    Returns:
        Lista filtrada de ventas
    """
    logger.debug(
        "Filtrando ventas - Categoría: %s, Región: %s, Fechas: %s - %s",
        categoria,
        region,
        fecha_inicio,
        fecha_fin,
    )

    resultado = ventas

    if categoria:
        resultado = [v for v in resultado if v.categoria.lower() == categoria.lower()]
        logger.debug("Filtro por categoría '%s': %d ventas", categoria, len(resultado))

    if region:
        resultado = [v for v in resultado if v.region.lower() == region.lower()]
        logger.debug("Filtro por región '%s': %d ventas", region, len(resultado))

    if fecha_inicio:
        resultado = [v for v in resultado if v.fecha >= fecha_inicio]
        logger.debug("Filtro por fecha inicio: %d ventas", len(resultado))

    if fecha_fin:
        resultado = [v for v in resultado if v.fecha <= fecha_fin]
        logger.debug("Filtro por fecha fin: %d ventas", len(resultado))

    logger.info("Filtrado completo: %d ventas (de %d originales)", len(resultado), len(ventas))

    return resultado


def exportar_json(
    metricas: MetricasVentas,
    ventas: list[Venta],
    archivo_salida: Path,
) -> None:
    """
    Exporta métricas y ventas a archivo JSON.

    Args:
        metricas: Métricas calculadas
        ventas: Lista de ventas
        archivo_salida: Ruta del archivo JSON de salida
    """
    logger.info("Exportando resultados a JSON: %s", archivo_salida)

    # Crear directorio si no existe
    archivo_salida.parent.mkdir(parents=True, exist_ok=True)

    # Preparar datos
    datos = {
        "metadata": {
            "generado_en": datetime.now().isoformat(),
            "total_registros": len(ventas),
            "version": "1.0",
        },
        "metricas": metricas.to_dict(),
        "ventas": [venta.to_dict() for venta in ventas],
    }

    try:
        with archivo_salida.open("w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

        logger.info(
            "JSON exportado exitosamente: %s (%.2f KB)",
            archivo_salida,
            archivo_salida.stat().st_size / 1024,
        )

    except Exception as e:
        logger.error("Error al exportar JSON: %s", e)
        raise


def imprimir_resumen(metricas: MetricasVentas) -> None:
    """Imprime resumen de métricas en consola."""
    print("\n" + "=" * 80)
    print(" " * 25 + "RESUMEN DE VENTAS")
    print("=" * 80)

    print(f"\nPeriodo: {metricas.periodo_inicio.date()} a {metricas.periodo_fin.date()}")
    print(f"Total de ventas: ${metricas.total_ventas:,.2f}")
    print(f"Transacciones: {metricas.cantidad_transacciones:,}")
    print(f"Ticket promedio: ${metricas.ticket_promedio:,.2f}")
    print(f"Venta mínima: ${metricas.venta_minima:,.2f}")
    print(f"Venta máxima: ${metricas.venta_maxima:,.2f}")
    print(f"Productos únicos: {metricas.productos_vendidos}")

    print("\n" + "-" * 80)
    print("VENTAS POR CATEGORÍA")
    print("-" * 80)
    for categoria, total in sorted(
        metricas.ventas_por_categoria.items(), key=lambda x: x[1], reverse=True
    ):
        porcentaje = (total / metricas.total_ventas) * 100
        print(f"{categoria:20} ${total:>12,.2f}  ({porcentaje:>5.1f}%)")

    print("\n" + "-" * 80)
    print("VENTAS POR REGIÓN")
    print("-" * 80)
    for region, total in sorted(
        metricas.ventas_por_region.items(), key=lambda x: x[1], reverse=True
    ):
        porcentaje = (total / metricas.total_ventas) * 100
        print(f"{region:20} ${total:>12,.2f}  ({porcentaje:>5.1f}%)")

    print("\n" + "-" * 80)
    print("TOP 5 PRODUCTOS")
    print("-" * 80)
    for i, (producto, total) in enumerate(metricas.top_productos[:5], 1):
        print(f"{i}. {producto:30} ${total:>12,.2f}")

    print("\n" + "-" * 80)
    print("TOP 5 VENDEDORES")
    print("-" * 80)
    for i, (vendedor, total) in enumerate(metricas.top_vendedores[:5], 1):
        print(f"{i}. {vendedor:30} ${total:>12,.2f}")

    print("\n" + "=" * 80 + "\n")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================


def main() -> None:
    """Función principal del procesador de ventas."""
    # Configurar logging con archivo
    directorio_logs = Path("logs")
    archivo_log = directorio_logs / "procesador_ventas.log"

    global logger
    logger = configurar_logging(nivel="DEBUG", archivo_log=archivo_log)

    logger.info("=" * 80)
    logger.info("Iniciando procesador de ventas")
    logger.info("=" * 80)

    try:
        # Rutas
        archivo_csv = Path("data/ventas_2024.csv")
        archivo_json = Path("output/metricas_ventas.json")

        # Leer CSV
        logger.info("Paso 1: Leyendo datos de CSV")
        ventas = leer_csv_ventas(archivo_csv)

        if not ventas:
            logger.error("No se pudieron leer ventas del archivo CSV")
            return

        # Calcular métricas
        logger.info("Paso 2: Calculando métricas")
        metricas = calcular_metricas(ventas)

        # Imprimir resumen
        logger.info("Paso 3: Generando resumen")
        imprimir_resumen(metricas)

        # Exportar JSON
        logger.info("Paso 4: Exportando a JSON")
        exportar_json(metricas, ventas, archivo_json)

        # Ejemplos de filtrado
        logger.info("Paso 5: Ejemplos de filtrado")

        # Filtrar por categoría
        ventas_electronica = filtrar_ventas(ventas, categoria="Electrónica")
        if ventas_electronica:
            metricas_electronica = calcular_metricas(ventas_electronica)
            logger.info(
                "Ventas de Electrónica: $%.2f (%d transacciones)",
                metricas_electronica.total_ventas,
                metricas_electronica.cantidad_transacciones,
            )

        # Filtrar por fecha (último trimestre)
        fecha_fin = metricas.periodo_fin
        fecha_inicio = fecha_fin - timedelta(days=90)
        ventas_trimestre = filtrar_ventas(ventas, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        if ventas_trimestre:
            metricas_trimestre = calcular_metricas(ventas_trimestre)
            logger.info(
                "Ventas último trimestre: $%.2f (%d transacciones)",
                metricas_trimestre.total_ventas,
                metricas_trimestre.cantidad_transacciones,
            )

        logger.info("=" * 80)
        logger.info("Procesamiento completado exitosamente")
        logger.info("Archivo JSON generado: %s", archivo_json.absolute())
        logger.info("Logs guardados en: %s", archivo_log.absolute())
        logger.info("=" * 80)

    except FileNotFoundError as e:
        logger.critical("Archivo no encontrado: %s", e)
        sys.exit(1)
    except ValueError as e:
        logger.critical("Error de valor: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.critical("Error inesperado: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
