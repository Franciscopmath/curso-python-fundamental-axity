#!/usr/bin/env python3
"""
Script de procesamiento de productos en formato JSON.

Este script demuestra:
- Lectura de archivos JSON con manejo de errores
- Filtrado y agregación de datos
- Uso de estructuras de datos (list, dict, set)
- Control de flujo (if, for, while)
- Manejo robusto de excepciones
- Argumentos de línea de comandos
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class ArchivoJSONError(Exception):
    """Excepción personalizada para errores de archivos JSON."""

    pass


class FormatoJSONError(Exception):
    """Excepción personalizada para errores de formato JSON."""

    pass


class ProcesadorProductos:
    """Clase para procesar datos de productos desde archivos JSON."""

    def __init__(self, ruta_archivo: str):
        """
        Inicializa el procesador con la ruta del archivo JSON.

        Args:
            ruta_archivo: Ruta al archivo JSON de productos

        Raises:
            ArchivoJSONError: Si hay problemas al leer el archivo
            FormatoJSONError: Si el JSON es inválido
        """
        self.ruta_archivo = Path(ruta_archivo)
        self.datos: dict[str, Any] = {}
        self.productos: list[dict[str, Any]] = []
        self._cargar_datos()

    def _cargar_datos(self) -> None:
        """
        Carga y valida los datos del archivo JSON.

        Raises:
            ArchivoJSONError: Si el archivo no existe o no se puede leer
            FormatoJSONError: Si el JSON es inválido o falta la clave 'productos'
        """
        try:
            # Verificar que el archivo existe
            if not self.ruta_archivo.exists():
                raise ArchivoJSONError(f"El archivo '{self.ruta_archivo}' no existe")

            # Verificar que es un archivo (no un directorio)
            if not self.ruta_archivo.is_file():
                raise ArchivoJSONError(f"'{self.ruta_archivo}' no es un archivo válido")

            # Leer el archivo JSON
            with open(self.ruta_archivo, encoding="utf-8") as archivo:
                self.datos = json.load(archivo)

            # Validar estructura del JSON
            if not isinstance(self.datos, dict):
                raise FormatoJSONError("El JSON debe ser un objeto/diccionario")

            if "productos" not in self.datos:
                raise FormatoJSONError("El JSON debe contener una clave 'productos'")

            if not isinstance(self.datos["productos"], list):
                raise FormatoJSONError("La clave 'productos' debe ser una lista")

            self.productos = self.datos["productos"]

            print(f"✅ Archivo cargado exitosamente: {len(self.productos)} productos")

        except FileNotFoundError:
            raise ArchivoJSONError(f"No se encontró el archivo: {self.ruta_archivo}")
        except PermissionError:
            raise ArchivoJSONError(f"Sin permisos para leer el archivo: {self.ruta_archivo}")
        except json.JSONDecodeError as e:
            raise FormatoJSONError(f"JSON inválido en línea {e.lineno}, columna {e.colno}: {e.msg}")
        except Exception as e:
            raise ArchivoJSONError(f"Error inesperado al leer archivo: {e}")

    def filtrar_por_categoria(self, categoria: str) -> list[dict[str, Any]]:
        """
        Filtra productos por categoría (case-insensitive).

        Args:
            categoria: Nombre de la categoría a filtrar

        Returns:
            Lista de productos que pertenecen a la categoría
        """
        categoria_lower = categoria.lower()
        filtrados = [p for p in self.productos if p.get("categoria", "").lower() == categoria_lower]
        print(f"🔍 Filtrados por categoría '{categoria}': {len(filtrados)} productos")
        return filtrados

    def filtrar_por_precio(
        self, precio_min: float | None = None, precio_max: float | None = None
    ) -> list[dict[str, Any]]:
        """
        Filtra productos por rango de precio.

        Args:
            precio_min: Precio mínimo (inclusivo)
            precio_max: Precio máximo (inclusivo)

        Returns:
            Lista de productos en el rango de precio
        """
        filtrados = self.productos.copy()

        if precio_min is not None:
            filtrados = [p for p in filtrados if p.get("precio", 0) >= precio_min]

        if precio_max is not None:
            filtrados = [p for p in filtrados if p.get("precio", 0) <= precio_max]

        rango = []
        if precio_min is not None:
            rango.append(f"≥${precio_min}")
        if precio_max is not None:
            rango.append(f"≤${precio_max}")

        print(f"🔍 Filtrados por precio {' y '.join(rango)}: {len(filtrados)} productos")
        return filtrados

    def filtrar_disponibles(self) -> list[dict[str, Any]]:
        """
        Filtra productos disponibles (disponible=True y stock>0).

        Returns:
            Lista de productos disponibles
        """
        filtrados = [
            p for p in self.productos if p.get("disponible", False) and p.get("stock", 0) > 0
        ]
        print(f"🔍 Productos disponibles: {len(filtrados)}")
        return filtrados

    def calcular_estadisticas(
        self, productos: list[dict[str, Any]] | None = None
    ) -> dict[str, Any]:
        """
        Calcula estadísticas de una lista de productos.

        Args:
            productos: Lista de productos (usa todos si es None)

        Returns:
            Diccionario con estadísticas calculadas
        """
        if productos is None:
            productos = self.productos

        if not productos:
            return {
                "total_productos": 0,
                "precio_promedio": 0,
                "precio_minimo": 0,
                "precio_maximo": 0,
                "stock_total": 0,
                "valor_inventario": 0,
            }

        precios = [p.get("precio", 0) for p in productos]
        stocks = [p.get("stock", 0) for p in productos]

        estadisticas = {
            "total_productos": len(productos),
            "precio_promedio": sum(precios) / len(precios) if precios else 0,
            "precio_minimo": min(precios) if precios else 0,
            "precio_maximo": max(precios) if precios else 0,
            "stock_total": sum(stocks),
            "valor_inventario": sum(p.get("precio", 0) * p.get("stock", 0) for p in productos),
        }

        return estadisticas

    def agrupar_por_categoria(self) -> dict[str, list[dict[str, Any]]]:
        """
        Agrupa productos por categoría.

        Returns:
            Diccionario donde la clave es la categoría y el valor es lista de productos
        """
        agrupados: dict[str, list[dict[str, Any]]] = {}

        for producto in self.productos:
            categoria = producto.get("categoria", "Sin categoría")
            if categoria not in agrupados:
                agrupados[categoria] = []
            agrupados[categoria].append(producto)

        print(f"📊 Productos agrupados en {len(agrupados)} categorías")
        return agrupados

    def obtener_categorias_unicas(self) -> set:
        """
        Obtiene el conjunto de categorías únicas.

        Returns:
            Set con nombres de categorías
        """
        categorias = {p.get("categoria", "Sin categoría") for p in self.productos}
        return categorias

    def buscar_por_etiqueta(self, etiqueta: str) -> list[dict[str, Any]]:
        """
        Busca productos que contengan una etiqueta específica.

        Args:
            etiqueta: Etiqueta a buscar

        Returns:
            Lista de productos con la etiqueta
        """
        etiqueta_lower = etiqueta.lower()
        productos_con_etiqueta = [
            p
            for p in self.productos
            if etiqueta_lower in [e.lower() for e in p.get("etiquetas", [])]
        ]

        print(f"🏷️  Productos con etiqueta '{etiqueta}': {len(productos_con_etiqueta)}")
        return productos_con_etiqueta

    def generar_reporte(self, productos: list[dict[str, Any]] | None = None) -> str:
        """
        Genera un reporte formateado de productos.

        Args:
            productos: Lista de productos (usa todos si es None)

        Returns:
            String con el reporte formateado
        """
        if productos is None:
            productos = self.productos

        if not productos:
            return "❌ No hay productos para mostrar"

        lineas = ["\n" + "=" * 100]
        lineas.append(f"📦 REPORTE DE PRODUCTOS ({len(productos)} productos)")
        lineas.append("=" * 100)

        for i, producto in enumerate(productos, 1):
            lineas.append(f"\n{i}. {producto.get('nombre', 'Sin nombre')}")
            lineas.append(f"   ID: {producto.get('id', 'N/A')}")
            lineas.append(f"   Categoría: {producto.get('categoria', 'N/A')}")
            lineas.append(f"   Precio: ${producto.get('precio', 0):.2f}")
            lineas.append(f"   Stock: {producto.get('stock', 0)} unidades")
            lineas.append(
                f"   Disponible: {'✅ Sí' if producto.get('disponible', False) else '❌ No'}"
            )

            if "etiquetas" in producto and producto["etiquetas"]:
                lineas.append(f"   Etiquetas: {', '.join(producto['etiquetas'])}")

        lineas.append("\n" + "=" * 100)

        # Agregar estadísticas
        stats = self.calcular_estadisticas(productos)
        lineas.append("\n📊 ESTADÍSTICAS:")
        lineas.append(f"   Total de productos: {stats['total_productos']}")
        lineas.append(f"   Precio promedio: ${stats['precio_promedio']:.2f}")
        lineas.append(
            f"   Rango de precios: ${stats['precio_minimo']:.2f} - ${stats['precio_maximo']:.2f}"
        )
        lineas.append(f"   Stock total: {stats['stock_total']} unidades")
        lineas.append(f"   Valor del inventario: ${stats['valor_inventario']:.2f}")
        lineas.append("=" * 100 + "\n")

        return "\n".join(lineas)


def configurar_argumentos() -> argparse.ArgumentParser:
    """
    Configura los argumentos de línea de comandos.

    Returns:
        Parser de argumentos configurado
    """
    parser = argparse.ArgumentParser(
        description="Procesa y filtra productos desde un archivo JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Mostrar todos los productos
  python procesador_productos.py productos.json

  # Filtrar por categoría
  python procesador_productos.py productos.json --categoria Electrónica

  # Filtrar por rango de precio
  python procesador_productos.py productos.json --precio-min 100 --precio-max 500

  # Solo productos disponibles
  python procesador_productos.py productos.json --disponibles

  # Buscar por etiqueta
  python procesador_productos.py productos.json --etiqueta gaming

  # Agrupar por categoría
  python procesador_productos.py productos.json --agrupar

  # Mostrar solo estadísticas
  python procesador_productos.py productos.json --estadisticas

  # Combinar filtros
  python procesador_productos.py productos.json --categoria Audio --disponibles
        """,
    )

    parser.add_argument("archivo", help="Ruta al archivo JSON de productos")

    parser.add_argument(
        "-c",
        "--categoria",
        help="Filtrar por categoría",
        metavar="CATEGORIA",
    )

    parser.add_argument(
        "--precio-min",
        type=float,
        help="Precio mínimo",
        metavar="PRECIO",
    )

    parser.add_argument(
        "--precio-max",
        type=float,
        help="Precio máximo",
        metavar="PRECIO",
    )

    parser.add_argument(
        "-d",
        "--disponibles",
        action="store_true",
        help="Mostrar solo productos disponibles",
    )

    parser.add_argument(
        "-e",
        "--etiqueta",
        help="Buscar por etiqueta",
        metavar="ETIQUETA",
    )

    parser.add_argument(
        "-a",
        "--agrupar",
        action="store_true",
        help="Agrupar productos por categoría",
    )

    parser.add_argument(
        "-s",
        "--estadisticas",
        action="store_true",
        help="Mostrar solo estadísticas (sin listado de productos)",
    )

    return parser


def main() -> int:
    """
    Función principal del programa.

    Returns:
        Código de salida (0 = éxito, 1 = error)
    """
    parser = configurar_argumentos()
    args = parser.parse_args()

    try:
        # Cargar datos
        procesador = ProcesadorProductos(args.archivo)

        # Aplicar filtros
        productos_filtrados = procesador.productos

        if args.categoria:
            productos_filtrados = procesador.filtrar_por_categoria(args.categoria)

        if args.precio_min is not None or args.precio_max is not None:
            productos_filtrados = [
                p
                for p in productos_filtrados
                if (args.precio_min is None or p.get("precio", 0) >= args.precio_min)
                and (args.precio_max is None or p.get("precio", 0) <= args.precio_max)
            ]
            print(f"🔍 Filtrados por precio: {len(productos_filtrados)} productos")

        if args.disponibles:
            productos_filtrados = [
                p
                for p in productos_filtrados
                if p.get("disponible", False) and p.get("stock", 0) > 0
            ]
            print(f"🔍 Disponibles: {len(productos_filtrados)} productos")

        if args.etiqueta:
            etiqueta_lower = args.etiqueta.lower()
            productos_filtrados = [
                p
                for p in productos_filtrados
                if etiqueta_lower in [e.lower() for e in p.get("etiquetas", [])]
            ]
            print(f"🏷️  Con etiqueta '{args.etiqueta}': {len(productos_filtrados)} productos")

        # Mostrar resultados
        if args.agrupar:
            # Agrupar productos filtrados
            agrupados: dict[str, list[dict[str, Any]]] = {}
            for producto in productos_filtrados:
                categoria = producto.get("categoria", "Sin categoría")
                if categoria not in agrupados:
                    agrupados[categoria] = []
                agrupados[categoria].append(producto)

            print("\n📊 Productos agrupados por categoría:\n")
            for categoria, productos in sorted(agrupados.items()):
                print(f"\n{categoria} ({len(productos)} productos):")
                for producto in productos:
                    print(f"  - {producto.get('nombre')} (${producto.get('precio', 0):.2f})")

        elif args.estadisticas:
            # Solo estadísticas
            stats = procesador.calcular_estadisticas(productos_filtrados)
            print("\n" + "=" * 60)
            print("📊 ESTADÍSTICAS")
            print("=" * 60)
            print(f"Total de productos: {stats['total_productos']}")
            print(f"Precio promedio: ${stats['precio_promedio']:.2f}")
            print(f"Precio mínimo: ${stats['precio_minimo']:.2f}")
            print(f"Precio máximo: ${stats['precio_maximo']:.2f}")
            print(f"Stock total: {stats['stock_total']} unidades")
            print(f"Valor del inventario: ${stats['valor_inventario']:.2f}")
            print("=" * 60 + "\n")

        else:
            # Reporte completo
            reporte = procesador.generar_reporte(productos_filtrados)
            print(reporte)

        return 0

    except ArchivoJSONError as e:
        print(f"\n❌ Error de archivo: {e}", file=sys.stderr)
        return 1
    except FormatoJSONError as e:
        print(f"\n❌ Error de formato JSON: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
