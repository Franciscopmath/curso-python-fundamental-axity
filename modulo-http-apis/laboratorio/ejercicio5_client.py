"""
Ejercicio 5: Cliente HTTP reutilizable.

Demuestra el uso de httpx.Client para reutilizar conexiones.
"""

from typing import Any

import httpx


class GitHubClient:
    """Cliente reutilizable para la API de GitHub."""

    def __init__(self, token: str | None = None):
        headers = {"Accept": "application/vnd.github.v3+json"}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.client = httpx.Client(
            base_url="https://api.github.com", headers=headers, timeout=10.0
        )

    def __enter__(self) -> "GitHubClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.client.close()

    def get_user(self, username: str) -> dict[str, Any]:
        """Obtiene información de un usuario."""
        response = self.client.get(f"/users/{username}")
        response.raise_for_status()
        return response.json()

    def get_repos(self, username: str, limit: int = 30) -> list[dict[str, Any]]:
        """Obtiene repositorios de un usuario."""
        response = self.client.get(
            f"/users/{username}/repos", params={"per_page": limit}
        )
        response.raise_for_status()
        return response.json()

    def search_repos(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Busca repositorios."""
        params = {"q": query, "per_page": limit}
        response = self.client.get("/search/repositories", params=params)
        response.raise_for_status()
        return response.json()["items"]

    def get_user_followers(self, username: str) -> list[dict[str, Any]]:
        """Obtiene los seguidores de un usuario."""
        response = self.client.get(f"/users/{username}/followers")
        response.raise_for_status()
        return response.json()

    def get_repo_issues(
        self, owner: str, repo: str, state: str = "open"
    ) -> list[dict[str, Any]]:
        """Obtiene los issues de un repositorio."""
        response = self.client.get(
            f"/repos/{owner}/{repo}/issues", params={"state": state}
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    with GitHubClient() as gh:
        # Obtener usuario
        print("=== Información de Usuario ===")
        user = gh.get_user("torvalds")
        print(f"Usuario: {user['name']}")
        print(f"Bio: {user.get('bio', 'N/A')}")
        print(f"Repos: {user['public_repos']}")
        print(f"Seguidores: {user['followers']}")

        # Obtener repositorios
        print("\n=== Repositorios ===")
        repos = gh.get_repos("torvalds", limit=5)
        print(f"Mostrando {len(repos)} repos:")
        for repo in repos:
            print(f"  - {repo['name']} (⭐ {repo['stargazers_count']})")

        # Buscar
        print("\n=== Búsqueda ===")
        results = gh.search_repos("linux kernel", limit=3)
        print("Búsqueda 'linux kernel':")
        for repo in results:
            print(f"  - {repo['full_name']} (⭐ {repo['stargazers_count']})")

        # Seguidores
        print("\n=== Seguidores ===")
        followers = gh.get_user_followers("torvalds")
        print("Primeros 5 seguidores de torvalds:")
        for follower in followers[:5]:
            print(f"  - {follower['login']}")

        # Issues de un repo
        print("\n=== Issues ===")
        try:
            issues = gh.get_repo_issues("python", "cpython", state="open")
            print(f"Issues abiertos en python/cpython: {len(issues)}")
            for issue in issues[:3]:
                print(f"  #{issue['number']}: {issue['title'][:60]}...")
        except httpx.HTTPStatusError as e:
            print(f"Error obteniendo issues: {e.response.status_code}")
