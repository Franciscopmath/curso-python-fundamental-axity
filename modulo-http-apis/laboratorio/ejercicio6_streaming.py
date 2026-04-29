"""
Ejercicio 6: Streaming de archivos grandes.

Demuestra descarga eficiente con barra de progreso.
"""

from pathlib import Path

import httpx

try:
    from tqdm import tqdm

    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


def descargar_archivo(url: str, destino: str) -> None:
    """Descarga un archivo mostrando progreso simple."""
    with httpx.stream("GET", url, timeout=30.0) as response:
        response.raise_for_status()

        # Obtener tamaño total
        total_size = int(response.headers.get("content-length", 0))

        if total_size == 0:
            print("Advertencia: Tamaño desconocido")

        downloaded = 0

        with open(destino, "wb") as f:
            for chunk in response.iter_bytes(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)

                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    mb_downloaded = downloaded / 1024 / 1024
                    mb_total = total_size / 1024 / 1024

                    print(
                        f"\rDescargando: {mb_downloaded:.2f}/{mb_total:.2f} MB "
                        f"({percent:.1f}%)",
                        end="",
                    )

        print(f"\n✓ Descarga completa: {destino}")


def descargar_con_tqdm(url: str, destino: str) -> None:
    """Descarga con barra de progreso usando tqdm."""
    if not TQDM_AVAILABLE:
        print("tqdm no disponible, usando método simple")
        descargar_archivo(url, destino)
        return

    with httpx.stream("GET", url, timeout=30.0) as response:
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))

        with open(destino, "wb") as f:
            with tqdm(
                total=total_size, unit="B", unit_scale=True, desc=Path(destino).name
            ) as pbar:
                for chunk in response.iter_bytes(chunk_size=8192):
                    f.write(chunk)
                    pbar.update(len(chunk))

        print("✓ Descarga completa")


def descargar_con_reintentos(url: str, destino: str, max_retries: int = 3) -> None:
    """Descarga con reintentos en caso de error."""
    for attempt in range(max_retries):
        try:
            print(f"Intento {attempt + 1}/{max_retries}...")

            if TQDM_AVAILABLE:
                descargar_con_tqdm(url, destino)
            else:
                descargar_archivo(url, destino)

            return  # Éxito

        except (httpx.HTTPError, OSError) as e:
            if attempt == max_retries - 1:
                raise
            print(f"\n✗ Error: {e}")
            print("Reintentando...\n")


if __name__ == "__main__":
    # Crear directorio para descargas
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)

    print("=== Descarga Simple ===\n")
    descargar_archivo(
        "https://httpbin.org/image/jpeg", str(downloads_dir / "imagen1.jpg")
    )

    print("\n" + "=" * 50 + "\n")

    if TQDM_AVAILABLE:
        print("=== Descarga con tqdm ===\n")
        descargar_con_tqdm(
            "https://httpbin.org/image/png", str(downloads_dir / "imagen2.png")
        )

        print("\n" + "=" * 50 + "\n")

    print("=== Descarga con Reintentos ===\n")
    descargar_con_reintentos(
        "https://httpbin.org/image/webp", str(downloads_dir / "imagen3.webp")
    )

    print(f"\n✓ Todos los archivos descargados en: {downloads_dir.absolute()}")
