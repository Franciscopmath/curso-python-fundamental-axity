"""
Ejercicio 4: Reintentos con backoff exponencial.

Implementa diferentes estrategias de reintento para APIs inestables.
"""

import random
import time
from collections.abc import Callable
from typing import TypeVar

import httpx

T = TypeVar("T")


def retry_with_backoff(
    func: Callable[[], T],
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    initial_delay: float = 1.0,
) -> T:
    """
    Reintenta una función con backoff exponencial.

    Args:
        func: Función a ejecutar
        max_retries: Número máximo de reintentos
        backoff_factor: Factor de multiplicación del delay
        initial_delay: Delay inicial en segundos

    Returns:
        Resultado de la función

    Raises:
        Exception: Si falla después de max_retries intentos
    """
    for attempt in range(max_retries):
        try:
            print(f"Intento {attempt + 1}/{max_retries}...")
            result = func()
            print(f"✓ Éxito en intento {attempt + 1}")
            return result

        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt == max_retries - 1:
                print(f"✗ Falló después de {max_retries} intentos")
                raise

            wait_time = initial_delay * (backoff_factor**attempt)
            print(f"✗ Error: {e}")
            print(f"  Esperando {wait_time:.1f}s antes de reintentar...\n")
            time.sleep(wait_time)

    raise RuntimeError("No debería llegar aquí")


def retry_exponential_jitter(
    func: Callable[[], T], max_retries: int = 3, base: float = 2.0
) -> T:
    """Backoff exponencial con jitter (aleatorio)."""
    for attempt in range(max_retries):
        try:
            result = func()
            print(f"✓ Éxito en intento {attempt + 1}")
            return result
        except Exception:
            if attempt == max_retries - 1:
                raise
            wait = (base**attempt) * (0.5 + random.random())
            print(f"Intento {attempt + 1} falló. Esperando {wait:.2f}s...")
            time.sleep(wait)

    raise RuntimeError("No debería llegar aquí")


def retry_solo_5xx(
    func: Callable[[], T], max_retries: int = 3, delay: float = 2.0
) -> T:
    """Solo reintenta en errores 5xx (errores de servidor)."""
    for attempt in range(max_retries):
        try:
            return func()
        except httpx.HTTPStatusError as e:
            # 4xx son errores del cliente, no reintentamos
            if 400 <= e.response.status_code < 500:
                print(f"Error 4xx ({e.response.status_code}): No reintentar")
                raise

            # 5xx son errores del servidor, reintentamos
            if attempt == max_retries - 1:
                raise

            print(
                f"Error 5xx ({e.response.status_code}): "
                f"Reintento {attempt + 1}/{max_retries}"
            )
            time.sleep(delay)

    raise RuntimeError("No debería llegar aquí")


def fetch_unstable_api() -> httpx.Response:
    """Simula una API inestable."""
    # httpbin.org/status responde con códigos aleatorios
    response = httpx.get("https://httpbin.org/status/200,503,503", timeout=5)
    response.raise_for_status()
    return response


def fetch_404() -> httpx.Response:
    """Intenta obtener un recurso que no existe (404)."""
    response = httpx.get("https://httpbin.org/status/404", timeout=5)
    response.raise_for_status()
    return response


if __name__ == "__main__":
    print("=== Estrategia: Backoff Exponencial ===\n")
    try:
        result = retry_with_backoff(fetch_unstable_api, max_retries=5)
        print(f"\n✓ API respondió: {result.status_code}\n")
    except Exception as e:
        print(f"\n✗ Falló definitivamente: {e}\n")

    print("=" * 50 + "\n")

    print("=== Estrategia: Backoff con Jitter ===\n")
    try:
        result = retry_exponential_jitter(fetch_unstable_api, max_retries=5)
        print(f"\n✓ API respondió: {result.status_code}\n")
    except Exception as e:
        print(f"\n✗ Falló definitivamente: {e}\n")

    print("=" * 50 + "\n")

    print("=== Estrategia: Solo reintentar 5xx ===\n")
    try:
        result = retry_solo_5xx(fetch_404, max_retries=3)
        print(f"✓ Respuesta: {result.status_code}")
    except httpx.HTTPStatusError as e:
        print(f"✗ Error 4xx no se reintenta: {e.response.status_code}")
