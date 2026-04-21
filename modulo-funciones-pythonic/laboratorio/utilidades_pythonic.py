#!/usr/bin/env python3
"""
Utilidades Pythonic: Decoradores, Generadores y Context Managers.

Este módulo implementa:
1. Decorador de reintentos con backoff exponencial
2. Generador por lotes (batch generator)
3. Context manager de temporización

Demuestra programación pythonic avanzada.
"""

import functools
import random
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any, TypeVar

# Type variables para decoradores
F = TypeVar("F", bound=Callable[..., Any])

# =============================================================================
# 1. DECORADOR DE REINTENTOS CON BACKOFF EXPONENCIAL
# =============================================================================


class ReintentosAgotadosError(Exception):
    """Excepción cuando se agotan los reintentos."""

    pass


def retry(
    max_intentos: int = 3,
    backoff_factor: float = 2.0,
    excepciones: tuple[type[Exception], ...] = (Exception,),
    jitter: bool = True,
) -> Callable[[F], F]:
    """
    Decorador que reintenta una función con backoff exponencial.

    Args:
        max_intentos: Número máximo de intentos (default: 3)
        backoff_factor: Factor de multiplicación para el backoff (default: 2.0)
        excepciones: Tupla de excepciones a capturar (default: (Exception,))
        jitter: Agregar variación aleatoria al delay (default: True)

    Returns:
        Función decorada con capacidad de reintentos

    Raises:
        ReintentosAgotadosError: Cuando se agotan los reintentos

    Example:
        >>> @retry(max_intentos=3, backoff_factor=2.0)
        ... def operacion_inestable():
        ...     if random.random() < 0.5:
        ...         raise ValueError("Error temporal")
        ...     return "Éxito"
    """

    def decorador(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            ultimos_error: Exception | None = None

            for intento in range(1, max_intentos + 1):
                try:
                    resultado = func(*args, **kwargs)
                    if intento > 1:
                        print(f"✅ Éxito en el intento {intento}")
                    return resultado

                except excepciones as e:
                    ultimos_error = e
                    if intento == max_intentos:
                        break

                    # Calcular delay con backoff exponencial
                    delay = backoff_factor ** (intento - 1)

                    # Agregar jitter (variación aleatoria)
                    if jitter:
                        delay *= 0.5 + random.random()  # 0.5x a 1.5x del delay

                    print(f"⚠️  Intento {intento}/{max_intentos} falló: {type(e).__name__}: {e}")
                    print(f"   Reintentando en {delay:.2f} segundos...")
                    time.sleep(delay)

            # Si llegamos aquí, se agotaron los reintentos
            raise ReintentosAgotadosError(
                f"Fallaron todos los {max_intentos} intentos. "
                f"Último error: {type(ultimos_error).__name__}: {ultimos_error}"
            ) from ultimos_error

        return wrapper  # type: ignore

    return decorador


def retry_async(max_intentos: int = 3, backoff_factor: float = 2.0) -> Callable[[F], F]:
    """
    Decorador de reintentos para funciones asíncronas.

    Similar a retry() pero para funciones async/await.

    Args:
        max_intentos: Número máximo de intentos
        backoff_factor: Factor de multiplicación para el backoff

    Returns:
        Función decorada con capacidad de reintentos
    """

    def decorador(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            import asyncio

            for intento in range(1, max_intentos + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception:
                    if intento == max_intentos:
                        raise
                    delay = backoff_factor ** (intento - 1)
                    print(f"Intento {intento} falló, reintentando en {delay}s...")
                    await asyncio.sleep(delay)

        return wrapper  # type: ignore

    return decorador


# =============================================================================
# 2. GENERADOR POR LOTES (BATCH GENERATOR)
# =============================================================================


def batch_generator(iterable: Iterator[Any], batch_size: int) -> Iterator[list[Any]]:
    """
    Generador que divide un iterable en lotes de tamaño fijo.

    Args:
        iterable: Cualquier iterable (lista, generador, etc.)
        batch_size: Tamaño de cada lote

    Yields:
        Listas de tamaño batch_size (el último puede ser menor)

    Raises:
        ValueError: Si batch_size es menor o igual a 0

    Example:
        >>> datos = range(10)
        >>> for lote in batch_generator(datos, 3):
        ...     print(lote)
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
        [9]
    """
    if batch_size <= 0:
        raise ValueError(f"batch_size debe ser > 0, recibido: {batch_size}")

    lote = []
    for item in iterable:
        lote.append(item)
        if len(lote) == batch_size:
            yield lote
            lote = []

    # Yield del último lote si no está vacío
    if lote:
        yield lote


def batch_generator_iterator(iterable: Iterator[Any], batch_size: int) -> Iterator[Iterator[Any]]:
    """
    Generador que retorna iteradores de lotes.

    Más eficiente en memoria que batch_generator() porque no crea listas.

    Args:
        iterable: Cualquier iterable
        batch_size: Tamaño de cada lote

    Yields:
        Iteradores de tamaño batch_size

    Example:
        >>> datos = range(10)
        >>> for lote in batch_generator_iterator(datos, 3):
        ...     print(list(lote))
    """
    from itertools import islice

    iterator = iter(iterable)
    while True:
        lote = list(islice(iterator, batch_size))
        if not lote:
            break
        yield iter(lote)


def chunked(iterable: Iterator[Any], size: int) -> Iterator[tuple[Any, ...]]:
    """
    Divide un iterable en chunks de tamaño fijo usando tuplas.

    Similar a batch_generator pero retorna tuplas en lugar de listas.

    Args:
        iterable: Cualquier iterable
        size: Tamaño de cada chunk

    Yields:
        Tuplas de tamaño 'size' (la última puede ser menor)

    Example:
        >>> for chunk in chunked(range(7), 3):
        ...     print(chunk)
        (0, 1, 2)
        (3, 4, 5)
        (6,)
    """
    from itertools import islice

    iterator = iter(iterable)
    while True:
        chunk = tuple(islice(iterator, size))
        if not chunk:
            break
        yield chunk


def windowed(iterable: Iterator[Any], size: int) -> Iterator[tuple[Any, ...]]:
    """
    Genera ventanas deslizantes de tamaño fijo.

    Args:
        iterable: Cualquier iterable
        size: Tamaño de la ventana

    Yields:
        Tuplas representando ventanas deslizantes

    Example:
        >>> for ventana in windowed(range(5), 3):
        ...     print(ventana)
        (0, 1, 2)
        (1, 2, 3)
        (2, 3, 4)
    """
    from collections import deque
    from itertools import islice

    iterator = iter(iterable)
    ventana = deque(islice(iterator, size), maxlen=size)

    if len(ventana) == size:
        yield tuple(ventana)

    for item in iterator:
        ventana.append(item)
        yield tuple(ventana)


# =============================================================================
# 3. CONTEXT MANAGERS DE TEMPORIZACIÓN
# =============================================================================


class Temporizador:
    """
    Context manager que mide el tiempo de ejecución de un bloque.

    Attributes:
        nombre: Nombre del bloque a medir
        silencioso: Si es True, no imprime automáticamente
        inicio: Timestamp de inicio
        fin: Timestamp de finalización
        duracion: Tiempo transcurrido en segundos

    Example:
        >>> with Temporizador("Operación lenta") as t:
        ...     time.sleep(1)
        ...     print("Procesando...")
        Procesando...
        ⏱️  Operación lenta: 1.0012 segundos

        >>> # Acceder a la duración
        >>> print(f"Duración: {t.duracion:.4f}s")
    """

    def __init__(self, nombre: str = "Bloque", silencioso: bool = False):
        """
        Inicializa el temporizador.

        Args:
            nombre: Nombre descriptivo del bloque
            silencioso: Si es True, no imprime el resultado
        """
        self.nombre = nombre
        self.silencioso = silencioso
        self.inicio: float = 0.0
        self.fin: float = 0.0
        self.duracion: float = 0.0

    def __enter__(self) -> "Temporizador":
        """Inicia el temporizador al entrar al bloque with."""
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, *args: Any) -> bool:
        """Detiene el temporizador al salir del bloque with."""
        self.fin = time.perf_counter()
        self.duracion = self.fin - self.inicio

        if not self.silencioso:
            print(f"⏱️  {self.nombre}: {self.duracion:.4f} segundos")

        return False  # No suprime excepciones

    def __str__(self) -> str:
        """Representación en string del temporizador."""
        return f"Temporizador('{self.nombre}', {self.duracion:.4f}s)"


@contextmanager
def temporizador(nombre: str = "Operación") -> Iterator[dict[str, Any]]:
    """
    Context manager funcional para medir tiempo de ejecución.

    Implementado usando @contextmanager para demostrar el enfoque funcional.

    Args:
        nombre: Nombre del bloque a medir

    Yields:
        Diccionario con información del temporizador

    Example:
        >>> with temporizador("Procesamiento") as info:
        ...     time.sleep(0.5)
        ...     print(f"Procesando...")
        Procesando...
        ⏱️  Procesamiento: 0.5001 segundos

        >>> print(info['duracion'])
        0.5001234
    """
    info: dict[str, Any] = {"nombre": nombre, "inicio": time.perf_counter()}

    try:
        yield info
    finally:
        info["fin"] = time.perf_counter()
        info["duracion"] = info["fin"] - info["inicio"]
        print(f"⏱️  {nombre}: {info['duracion']:.4f} segundos")


class TemporizadorAcumulativo:
    """
    Context manager que acumula tiempos de múltiples ejecuciones.

    Útil para medir el tiempo total de operaciones repetidas.

    Example:
        >>> timer = TemporizadorAcumulativo("Operaciones DB")
        >>> for i in range(3):
        ...     with timer:
        ...         time.sleep(0.1)
        >>> print(f"Total: {timer.total:.2f}s en {timer.veces} ejecuciones")
        Total: 0.30s en 3 ejecuciones
    """

    def __init__(self, nombre: str = "Operación"):
        """
        Inicializa el temporizador acumulativo.

        Args:
            nombre: Nombre descriptivo
        """
        self.nombre = nombre
        self.total: float = 0.0
        self.veces: int = 0
        self._inicio: float = 0.0

    def __enter__(self) -> "TemporizadorAcumulativo":
        """Inicia medición."""
        self._inicio = time.perf_counter()
        return self

    def __exit__(self, *args: Any) -> bool:
        """Acumula el tiempo transcurrido."""
        duracion = time.perf_counter() - self._inicio
        self.total += duracion
        self.veces += 1
        return False

    @property
    def promedio(self) -> float:
        """Calcula el tiempo promedio por ejecución."""
        return self.total / self.veces if self.veces > 0 else 0.0

    def __str__(self) -> str:
        """Representación en string."""
        return (
            f"TemporizadorAcumulativo('{self.nombre}': "
            f"total={self.total:.4f}s, veces={self.veces}, "
            f"promedio={self.promedio:.4f}s)"
        )

    def reporte(self) -> str:
        """Genera un reporte detallado."""
        if self.veces == 0:
            return f"{self.nombre}: Sin ejecuciones"

        return (
            f"\n📊 Reporte: {self.nombre}\n"
            f"   • Ejecuciones: {self.veces}\n"
            f"   • Tiempo total: {self.total:.4f}s\n"
            f"   • Tiempo promedio: {self.promedio:.4f}s\n"
            f"   • Tiempo mínimo: {self.total / self.veces if self.veces > 0 else 0:.4f}s\n"
        )


# =============================================================================
# FUNCIONES DE DEMOSTRACIÓN
# =============================================================================


def funcion_inestable(probabilidad_fallo: float = 0.7) -> str:
    """
    Función que falla aleatoriamente para demostrar el decorador de reintentos.

    Args:
        probabilidad_fallo: Probabilidad de fallo (0.0 a 1.0)

    Returns:
        Mensaje de éxito

    Raises:
        ValueError: Cuando falla la operación
    """
    if random.random() < probabilidad_fallo:
        raise ValueError(f"Fallo simulado (probabilidad: {probabilidad_fallo})")
    return "✅ Operación exitosa"


@retry(max_intentos=5, backoff_factor=1.5, excepciones=(ValueError,))
def operacion_con_retry() -> str:
    """Operación que se reintenta automáticamente en caso de fallo."""
    return funcion_inestable(probabilidad_fallo=0.6)


def procesar_lote(lote: list[int]) -> int:
    """
    Procesa un lote de números.

    Args:
        lote: Lista de números

    Returns:
        Suma del lote
    """
    print(f"  Procesando lote de {len(lote)} elementos: {lote}")
    time.sleep(0.1)  # Simular procesamiento
    return sum(lote)


def ejemplo_generador_lotes() -> None:
    """Demuestra el uso del generador por lotes."""
    print("\n" + "=" * 80)
    print("EJEMPLO: Generador por Lotes")
    print("=" * 80)

    datos = range(25)
    print(f"\n📦 Procesando {len(list(datos))} elementos en lotes de 5...\n")

    total = 0
    for i, lote in enumerate(batch_generator(range(25), batch_size=5), 1):
        print(f"Lote {i}:")
        resultado = procesar_lote(lote)
        total += resultado
        print(f"  → Suma del lote: {resultado}\n")

    print(f"✅ Suma total: {total}")


def ejemplo_temporizador() -> None:
    """Demuestra el uso de los context managers de temporización."""
    print("\n" + "=" * 80)
    print("EJEMPLO: Context Managers de Temporización")
    print("=" * 80)

    # 1. Temporizador básico
    print("\n1️⃣  Temporizador básico:")
    with Temporizador("Operación simple"):
        time.sleep(0.5)
        print("   Procesando datos...")

    # 2. Temporizador funcional
    print("\n2️⃣  Temporizador funcional (@contextmanager):")
    with temporizador("Cálculo complejo"):
        suma = sum(range(1000000))
        print(f"   Suma calculada: {suma}")

    # 3. Temporizador acumulativo
    print("\n3️⃣  Temporizador acumulativo:")
    timer = TemporizadorAcumulativo("Consultas DB")

    for i in range(3):
        with timer:
            print(f"   Consulta {i + 1}...")
            time.sleep(0.1 + random.random() * 0.1)

    print(timer.reporte())


def ejemplo_retry() -> None:
    """Demuestra el uso del decorador de reintentos."""
    print("\n" + "=" * 80)
    print("EJEMPLO: Decorador de Reintentos con Backoff")
    print("=" * 80)

    print("\n🔄 Intentando operación inestable con retry...\n")

    try:
        resultado = operacion_con_retry()
        print(f"\n{resultado}")
    except ReintentosAgotadosError as e:
        print(f"\n❌ {e}")


# =============================================================================
# EJEMPLOS ADICIONALES
# =============================================================================


def ejemplo_windowed() -> None:
    """Demuestra ventanas deslizantes."""
    print("\n" + "=" * 80)
    print("EJEMPLO: Ventanas Deslizantes")
    print("=" * 80)

    datos = [1, 2, 3, 4, 5]
    print(f"\nDatos: {datos}")
    print("Ventanas de tamaño 3:\n")

    for i, ventana in enumerate(windowed(datos, 3), 1):
        print(f"  Ventana {i}: {ventana}")


def ejemplo_chunked() -> None:
    """Demuestra chunked con tuplas."""
    print("\n" + "=" * 80)
    print("EJEMPLO: Chunked (chunks con tuplas)")
    print("=" * 80)

    datos = range(10)
    print("\nDatos: 0-9")
    print("Chunks de tamaño 3:\n")

    for i, chunk in enumerate(chunked(datos, 3), 1):
        print(f"  Chunk {i}: {chunk}")


# =============================================================================
# MAIN - EJECUTAR TODOS LOS EJEMPLOS
# =============================================================================


def main() -> None:
    """Ejecuta todos los ejemplos de demostración."""
    print("\n" + "=" * 80)
    print(" " * 20 + "LABORATORIO: FUNCIONES PYTHONIC")
    print("=" * 80)
    print("\nDemostraciones de:")
    print("  1. Decorador de reintentos con backoff exponencial")
    print("  2. Generadores por lotes")
    print("  3. Context managers de temporización")
    print("  4. Ventanas deslizantes y chunking")

    # Ejecutar ejemplos
    ejemplo_retry()
    ejemplo_generador_lotes()
    ejemplo_temporizador()
    ejemplo_windowed()
    ejemplo_chunked()

    print("\n" + "=" * 80)
    print("✅ Todos los ejemplos completados exitosamente")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
