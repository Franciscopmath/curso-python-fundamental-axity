"""
Ejercicio 2: Operaciones CRUD con JSONPlaceholder.

Demuestra POST, PUT, PATCH y DELETE.
"""

from typing import Any

import httpx

BASE_URL = "https://jsonplaceholder.typicode.com"


def crear_post(title: str, body: str, user_id: int = 1) -> dict[str, Any]:
    """Crea un nuevo post."""
    url = f"{BASE_URL}/posts"

    data = {"title": title, "body": body, "userId": user_id}

    response = httpx.post(url, json=data, timeout=10.0)
    response.raise_for_status()

    return response.json()


def actualizar_post(post_id: int, title: str, body: str) -> dict[str, Any]:
    """Actualiza un post existente (PUT - reemplazo completo)."""
    url = f"{BASE_URL}/posts/{post_id}"

    data = {"title": title, "body": body, "userId": 1}

    response = httpx.put(url, json=data, timeout=10.0)
    response.raise_for_status()

    return response.json()


def actualizar_parcial(post_id: int, **kwargs: Any) -> dict[str, Any]:
    """Actualiza parcialmente un post (PATCH)."""
    url = f"{BASE_URL}/posts/{post_id}"

    response = httpx.patch(url, json=kwargs, timeout=10.0)
    response.raise_for_status()

    return response.json()


def eliminar_post(post_id: int) -> None:
    """Elimina un post."""
    url = f"{BASE_URL}/posts/{post_id}"

    response = httpx.delete(url, timeout=10.0)
    response.raise_for_status()

    print(f"Post {post_id} eliminado (status: {response.status_code})")


def obtener_posts_usuario(user_id: int) -> list[dict[str, Any]]:
    """Obtiene todos los posts de un usuario."""
    url = f"{BASE_URL}/posts"
    params = {"userId": user_id}

    response = httpx.get(url, params=params, timeout=10.0)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    try:
        # Crear
        print("1. Creando post...")
        nuevo_post = crear_post("Mi primer post", "Este es el contenido de mi post")
        print(f"✓ Post creado con ID: {nuevo_post['id']}\n")

        # Actualizar completo
        print("2. Actualizando post completo (PUT)...")
        post_id = nuevo_post["id"]
        post_actualizado = actualizar_post(
            post_id, "Título actualizado", "Contenido actualizado"
        )
        print(f"✓ Post {post_id} actualizado\n")

        # Actualizar parcial
        print("3. Actualizando solo título (PATCH)...")
        post_parcial = actualizar_parcial(post_id, title="Solo título nuevo")
        print(f"✓ Título actualizado: {post_parcial.get('title')}\n")

        # Listar posts de usuario
        print("4. Obteniendo posts del usuario 1...")
        posts = obtener_posts_usuario(1)
        print(f"✓ Usuario tiene {len(posts)} posts")
        for post in posts[:3]:
            print(f"  - {post['title'][:50]}...")
        print()

        # Eliminar
        print("5. Eliminando post...")
        eliminar_post(post_id)

    except httpx.HTTPStatusError as e:
        print(f"Error HTTP: {e.response.status_code}")
        print(f"Respuesta: {e.response.text}")
    except httpx.RequestError as e:
        print(f"Error en request: {e}")
