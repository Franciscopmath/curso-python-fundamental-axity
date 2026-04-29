"""
Ejercicio 3: Manejo robusto de errores y timeouts.

Demuestra diferentes tipos de errores HTTP y cómo manejarlos.
"""

import logging
from typing import Any

import httpx

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def fetch_data_robusto(url: str) -> dict[str, Any] | None:
    """Request con manejo completo de errores."""

    try:
        logger.info(f"Intentando conectar a: {url}")

        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()

        logger.info(f"✓ Respuesta exitosa: {response.status_code}")
        return response.json()

    except httpx.ConnectTimeout:
        logger.error("✗ Timeout al conectar al servidor")

    except httpx.ReadTimeout:
        logger.error("✗ Timeout al leer la respuesta")

    except httpx.TimeoutException:
        logger.error("✗ Timeout general")

    except httpx.HTTPStatusError as e:
        logger.error(f"✗ Error HTTP {e.response.status_code}: {e.response.text[:100]}")

    except httpx.NetworkError as e:
        logger.error(f"✗ Error de red: {e}")

    except httpx.RequestError as e:
        logger.error(f"✗ Error en request: {e}")

    except Exception as e:
        logger.error(f"✗ Error inesperado: {e}")

    return None


def test_timeouts() -> None:
    """Prueba diferentes configuraciones de timeout."""
    # URL que simula delay
    url_delay = "https://httpbin.org/delay/5"

    print("1. Timeout muy corto (3 segundos):")
    try:
        response = httpx.get(url_delay, timeout=3.0)
        print(f"   ✓ Respuesta recibida: {response.status_code}")
    except httpx.TimeoutException:
        print("   ✗ Timeout! La respuesta tardó más de 3 segundos")

    print("\n2. Timeout adecuado (10 segundos):")
    try:
        response = httpx.get(url_delay, timeout=10.0)
        print(f"   ✓ Respuesta recibida: {response.status_code}")
    except httpx.TimeoutException:
        print("   ✗ Timeout!")

    print("\n3. Timeouts granulares:")
    timeout = httpx.Timeout(connect=5.0, read=10.0, write=5.0, pool=5.0)
    try:
        response = httpx.get(url_delay, timeout=timeout)
        print(f"   ✓ Respuesta recibida: {response.status_code}")
    except httpx.TimeoutException:
        print("   ✗ Timeout!")


if __name__ == "__main__":
    print("=== Pruebas de Manejo de Errores ===\n")

    # Exitoso
    print("Test 1: Request exitoso")
    fetch_data_robusto("https://api.github.com/users/octocat")

    print("\n" + "=" * 50 + "\n")

    # 404
    print("Test 2: Error 404")
    fetch_data_robusto("https://api.github.com/users/este-usuario-no-existe-12345")

    print("\n" + "=" * 50 + "\n")

    # URL inválida
    print("Test 3: Dominio inexistente")
    fetch_data_robusto("https://dominio-que-no-existe-12345.com")

    print("\n" + "=" * 50 + "\n")

    # Timeouts
    print("Test 4: Configuraciones de timeout")
    test_timeouts()
