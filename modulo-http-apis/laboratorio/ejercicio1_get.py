"""
Ejercicio 1: Request GET simple con httpx.

Obtiene información de usuarios de GitHub.
"""

import httpx


def obtener_usuario_github(username: str) -> None:
    """Obtiene información de un usuario de GitHub."""
    url = f"https://api.github.com/users/{username}"

    response = httpx.get(url, timeout=10.0)

    if response.status_code == 200:
        data = response.json()
        print(f"Nombre: {data.get('name', 'N/A')}")
        print(f"Bio: {data.get('bio', 'N/A')}")
        print(f"Repos públicos: {data.get('public_repos', 0)}")
        print(f"Seguidores: {data.get('followers', 0)}")
        print(f"Company: {data.get('company', 'N/A')}")
        print(f"Location: {data.get('location', 'N/A')}")
        print(f"Creado: {data.get('created_at', 'N/A')}")
    elif response.status_code == 404:
        print(f"Usuario '{username}' no encontrado")
    else:
        print(f"Error: {response.status_code}")


if __name__ == "__main__":
    print("=== Usuario: torvalds ===")
    obtener_usuario_github("torvalds")

    print("\n=== Usuario: gvanrossum ===")
    obtener_usuario_github("gvanrossum")

    print("\n=== Usuario inexistente ===")
    obtener_usuario_github("este-usuario-no-existe-12345")
