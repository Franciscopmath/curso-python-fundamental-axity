# Laboratorio: HTTP y Consumo de APIs

## Objetivos

Al completar este laboratorio serás capaz de:
- Consumir APIs REST con httpx
- Manejar errores y timeouts apropiadamente
- Implementar reintentos con backoff exponencial
- Autenticar requests a APIs
- Descargar archivos grandes con streaming
- Procesar datos de APIs públicas

---

## Ejercicio 1: Primeros Pasos con httpx

### 1.1 Instalación y Setup

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install httpx
```

### 1.2 Request GET Simple

Crea `ejercicio1_get.py`:

```python
import httpx

def obtener_usuario_github(username: str):
    """Obtiene información de un usuario de GitHub."""
    url = f"https://api.github.com/users/{username}"

    response = httpx.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Nombre: {data['name']}")
        print(f"Bio: {data['bio']}")
        print(f"Repos públicos: {data['public_repos']}")
        print(f"Seguidores: {data['followers']}")
    elif response.status_code == 404:
        print(f"Usuario '{username}' no encontrado")
    else:
        print(f"Error: {response.status_code}")

# Prueba
obtener_usuario_github("torvalds")
```

**Tareas:**
1. ✅ Ejecuta el script y observa la salida
2. ✅ Prueba con tu propio usuario de GitHub
3. ✅ Prueba con un usuario que no exista
4. ✅ Modifica para mostrar también: `company`, `location`, `created_at`

### 1.3 Request con Parámetros

Crea `ejercicio1_params.py`:

```python
import httpx
from typing import Dict, List

def buscar_repositorios(query: str, sort: str = "stars", limit: int = 5):
    """Busca repositorios en GitHub."""
    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "sort": sort,
        "order": "desc",
        "per_page": limit
    }

    response = httpx.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    print(f"Total encontrados: {data['total_count']}")
    print(f"\nTop {limit} repositorios:\n")

    for i, repo in enumerate(data['items'], 1):
        print(f"{i}. {repo['full_name']}")
        print(f"   ⭐ {repo['stargazers_count']} | "
              f"🍴 {repo['forks_count']} | "
              f"📝 {repo['description'][:60] if repo['description'] else 'Sin descripción'}")
        print()

# Prueba
buscar_repositorios("python machine learning")
```

**Tareas:**
1. ✅ Busca repositorios de "fastapi"
2. ✅ Ordena por "forks" en lugar de "stars"
3. ✅ Agrega filtro por lenguaje (usa `q="python language:python"`)
4. ✅ Muestra también la fecha de última actualización

---

## Ejercicio 2: POST, PUT, DELETE

### 2.1 API de Prueba: JSONPlaceholder

Crea `ejercicio2_crud.py`:

```python
import httpx
from typing import Dict

BASE_URL = "https://jsonplaceholder.typicode.com"

def crear_post(title: str, body: str, user_id: int = 1) -> Dict:
    """Crea un nuevo post."""
    url = f"{BASE_URL}/posts"

    data = {
        "title": title,
        "body": body,
        "userId": user_id
    }

    response = httpx.post(url, json=data)
    response.raise_for_status()

    return response.json()

def actualizar_post(post_id: int, title: str, body: str) -> Dict:
    """Actualiza un post existente."""
    url = f"{BASE_URL}/posts/{post_id}"

    data = {
        "title": title,
        "body": body,
        "userId": 1
    }

    response = httpx.put(url, json=data)
    response.raise_for_status()

    return response.json()

def eliminar_post(post_id: int):
    """Elimina un post."""
    url = f"{BASE_URL}/posts/{post_id}"

    response = httpx.delete(url)
    response.raise_for_status()

    print(f"Post {post_id} eliminado (status: {response.status_code})")

# Prueba el flujo completo
if __name__ == "__main__":
    # Crear
    nuevo_post = crear_post(
        "Mi primer post",
        "Este es el contenido de mi post"
    )
    print(f"✓ Post creado con ID: {nuevo_post['id']}\n")

    # Actualizar
    post_id = nuevo_post['id']
    post_actualizado = actualizar_post(
        post_id,
        "Título actualizado",
        "Contenido actualizado"
    )
    print(f"✓ Post {post_id} actualizado\n")

    # Eliminar
    eliminar_post(post_id)
```

**Tareas:**
1. ✅ Crea una función `actualizar_parcial()` usando PATCH
2. ✅ Crea una función `obtener_posts_usuario(user_id)` que liste todos los posts de un usuario
3. ✅ Agrega manejo de errores con try/except

---

## Ejercicio 3: Manejo de Errores y Timeouts

### 3.1 Timeouts

Crea `ejercicio3_timeouts.py`:

```python
import httpx
import time

def test_timeout():
    """Prueba diferentes configuraciones de timeout."""

    # URL que simula delay
    url = "https://httpbin.org/delay/5"  # Responde después de 5 segundos

    print("1. Request sin timeout (peligroso):")
    try:
        response = httpx.get(url, timeout=None)
        print(f"   ✓ Respuesta recibida: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    print("\n2. Timeout muy corto (3 segundos):")
    try:
        response = httpx.get(url, timeout=3.0)
        print(f"   ✓ Respuesta recibida: {response.status_code}")
    except httpx.TimeoutException:
        print(f"   ✗ Timeout! La respuesta tardó más de 3 segundos")

    print("\n3. Timeout adecuado (10 segundos):")
    try:
        response = httpx.get(url, timeout=10.0)
        print(f"   ✓ Respuesta recibida: {response.status_code}")
    except httpx.TimeoutException:
        print(f"   ✗ Timeout!")

    print("\n4. Timeouts granulares:")
    timeout = httpx.Timeout(
        connect=5.0,  # 5s para conectar
        read=10.0,    # 10s para leer
        write=5.0,    # 5s para escribir
        pool=5.0      # 5s esperando conexión del pool
    )
    try:
        response = httpx.get(url, timeout=timeout)
        print(f"   ✓ Respuesta recibida: {response.status_code}")
    except httpx.TimeoutException:
        print(f"   ✗ Timeout!")

if __name__ == "__main__":
    test_timeout()
```

### 3.2 Manejo Robusto de Errores

Crea `ejercicio3_errores.py`:

```python
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_data_robusto(url: str):
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

# Pruebas
if __name__ == "__main__":
    # Exitoso
    fetch_data_robusto("https://api.github.com/users/octocat")

    # 404
    fetch_data_robusto("https://api.github.com/users/este-usuario-no-existe-12345")

    # Timeout
    fetch_data_robusto("https://httpbin.org/delay/15")

    # URL inválida
    fetch_data_robusto("https://dominio-que-no-existe-12345.com")
```

**Tareas:**
1. ✅ Modifica para retornar un diccionario con `{"success": bool, "data": any, "error": str}`
2. ✅ Agrega un parámetro `retries` para reintentar automáticamente
3. ✅ Prueba con diferentes URLs problemáticas

---

## Ejercicio 4: Reintentos y Backoff

### 4.1 Implementación Manual

Crea `ejercicio4_reintentos.py`:

```python
import httpx
import time
from typing import Callable, Optional

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    initial_delay: float = 1.0
):
    """
    Reintenta una función con backoff exponencial.

    Args:
        func: Función a ejecutar
        max_retries: Número máximo de reintentos
        backoff_factor: Factor de multiplicación del delay
        initial_delay: Delay inicial en segundos
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

            wait_time = initial_delay * (backoff_factor ** attempt)
            print(f"✗ Error: {e}")
            print(f"  Esperando {wait_time:.1f}s antes de reintentar...\n")
            time.sleep(wait_time)

def fetch_unstable_api():
    """Simula una API inestable."""
    # httpbin.org/status/200,503,503 retorna 200 1/3 veces, 503 2/3 veces
    response = httpx.get("https://httpbin.org/status/200,503,503", timeout=5)
    response.raise_for_status()
    return response

# Prueba
if __name__ == "__main__":
    try:
        result = retry_with_backoff(fetch_unstable_api, max_retries=5)
        print(f"\n✓ API respondió correctamente: {result.status_code}")
    except Exception as e:
        print(f"\n✗ Falló definitivamente: {e}")
```

### 4.2 Estrategias de Reintento

Crea `ejercicio4_estrategias.py`:

```python
import httpx
import time
import random

def retry_linear(func, max_retries=3, delay=1.0):
    """Backoff lineal: 1s, 2s, 3s..."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait = delay * (attempt + 1)
            print(f"Intento {attempt + 1} falló. Esperando {wait}s...")
            time.sleep(wait)

def retry_exponential(func, max_retries=3, base=2.0):
    """Backoff exponencial: 1s, 2s, 4s, 8s..."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait = base ** attempt
            print(f"Intento {attempt + 1} falló. Esperando {wait}s...")
            time.sleep(wait)

def retry_exponential_jitter(func, max_retries=3, base=2.0):
    """Backoff exponencial con jitter (aleatorio)."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait = (base ** attempt) * (0.5 + random.random())
            print(f"Intento {attempt + 1} falló. Esperando {wait:.2f}s...")
            time.sleep(wait)

# Prueba las tres estrategias
def api_inestable():
    response = httpx.get("https://httpbin.org/status/200,503", timeout=5)
    response.raise_for_status()
    return response

if __name__ == "__main__":
    print("=== Estrategia Lineal ===")
    retry_linear(api_inestable, max_retries=4)

    print("\n=== Estrategia Exponencial ===")
    retry_exponential(api_inestable, max_retries=4)

    print("\n=== Estrategia Exponencial + Jitter ===")
    retry_exponential_jitter(api_inestable, max_retries=4)
```

**Tareas:**
1. ✅ Implementa una función que solo reintente en errores 5xx, no en 4xx
2. ✅ Agrega un parámetro `max_wait_time` para limitar el tiempo máximo de espera
3. ✅ Implementa respeto al header `Retry-After` si existe

---

## Ejercicio 5: Client Reutilizable

### 5.1 Cliente con Configuración

Crea `ejercicio5_client.py`:

```python
import httpx
from typing import Dict, List, Optional

class GitHubClient:
    """Cliente reutilizable para la API de GitHub."""

    def __init__(self, token: Optional[str] = None):
        headers = {"Accept": "application/vnd.github.v3+json"}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.client = httpx.Client(
            base_url="https://api.github.com",
            headers=headers,
            timeout=10.0
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_user(self, username: str) -> Dict:
        """Obtiene información de un usuario."""
        response = self.client.get(f"/users/{username}")
        response.raise_for_status()
        return response.json()

    def get_repos(self, username: str) -> List[Dict]:
        """Obtiene repositorios de un usuario."""
        response = self.client.get(f"/users/{username}/repos")
        response.raise_for_status()
        return response.json()

    def search_repos(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca repositorios."""
        params = {"q": query, "per_page": limit}
        response = self.client.get("/search/repositories", params=params)
        response.raise_for_status()
        return response.json()["items"]

# Uso
if __name__ == "__main__":
    with GitHubClient() as gh:
        # Obtener usuario
        user = gh.get_user("torvalds")
        print(f"Usuario: {user['name']}")
        print(f"Repos: {user['public_repos']}")

        # Obtener repositorios
        repos = gh.get_repos("torvalds")
        print(f"\nPrimeros 5 repos:")
        for repo in repos[:5]:
            print(f"  - {repo['name']} (⭐ {repo['stargazers_count']})")

        # Buscar
        results = gh.search_repos("linux kernel", limit=3)
        print(f"\nBúsqueda 'linux kernel':")
        for repo in results:
            print(f"  - {repo['full_name']}")
```

**Tareas:**
1. ✅ Agrega método `get_user_followers(username)`
2. ✅ Agrega método `get_repo_issues(owner, repo)`
3. ✅ Implementa paginación en `get_repos()` para obtener más de 30 repos
4. ✅ Agrega logging de todas las requests realizadas

---

## Ejercicio 6: Streaming de Archivos

### 6.1 Descarga con Progreso

Crea `ejercicio6_streaming.py`:

```python
import httpx
from pathlib import Path

def descargar_archivo(url: str, destino: str):
    """Descarga un archivo mostrando progreso."""

    with httpx.stream("GET", url) as response:
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

                    print(f"\rDescargando: {mb_downloaded:.2f}/{mb_total:.2f} MB "
                          f"({percent:.1f}%)", end="")

        print(f"\n✓ Descarga completa: {destino}")

# Prueba con una imagen
if __name__ == "__main__":
    url = "https://httpbin.org/image/jpeg"
    descargar_archivo(url, "imagen.jpg")
```

### 6.2 Con tqdm

Crea `ejercicio6_tqdm.py`:

```bash
pip install tqdm
```

```python
import httpx
from tqdm import tqdm

def descargar_con_tqdm(url: str, destino: str):
    """Descarga con barra de progreso usando tqdm."""

    with httpx.stream("GET", url) as response:
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))

        with open(destino, "wb") as f:
            with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc=destino
            ) as pbar:
                for chunk in response.iter_bytes(chunk_size=8192):
                    f.write(chunk)
                    pbar.update(len(chunk))

        print(f"✓ Descarga completa")

# Prueba
if __name__ == "__main__":
    # Descarga Python logo
    descargar_con_tqdm(
        "https://www.python.org/static/community_logos/python-logo.png",
        "python-logo.png"
    )
```

**Tareas:**
1. ✅ Agrega manejo de errores (reintentar si falla)
2. ✅ Implementa descarga resumible (continuar si se interrumpe)
3. ✅ Agrega validación de hash MD5/SHA256 después de descargar

---

## Ejercicio 7: Async con httpx

### 7.1 Requests Concurrentes

Crea `ejercicio7_async.py`:

```python
import httpx
import asyncio
import time

async def fetch_user(username: str) -> dict:
    """Obtiene un usuario de GitHub (async)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.github.com/users/{username}")
        response.raise_for_status()
        return response.json()

async def fetch_multiple_users_sequential(usernames: list[str]):
    """Obtiene usuarios secuencialmente."""
    print("=== Secuencial ===")
    start = time.time()

    users = []
    for username in usernames:
        user = await fetch_user(username)
        users.append(user)
        print(f"  ✓ {username}")

    elapsed = time.time() - start
    print(f"Tiempo: {elapsed:.2f}s\n")
    return users

async def fetch_multiple_users_concurrent(usernames: list[str]):
    """Obtiene usuarios concurrentemente."""
    print("=== Concurrente ===")
    start = time.time()

    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f"https://api.github.com/users/{username}")
            for username in usernames
        ]
        responses = await asyncio.gather(*tasks)
        users = [r.json() for r in responses]

    elapsed = time.time() - start
    print(f"  ✓ {len(users)} usuarios obtenidos")
    print(f"Tiempo: {elapsed:.2f}s\n")
    return users

# Prueba
if __name__ == "__main__":
    usernames = ["torvalds", "gvanrossum", "octocat", "kentcdodds", "tj"]

    # Secuencial
    asyncio.run(fetch_multiple_users_sequential(usernames))

    # Concurrente (mucho más rápido)
    asyncio.run(fetch_multiple_users_concurrent(usernames))
```

**Tareas:**
1. ✅ Implementa manejo de errores (que un usuario falle no detenga los demás)
2. ✅ Agrega límite de concurrencia (máximo N requests simultáneas)
3. ✅ Mide la diferencia de tiempo entre secuencial y concurrente

---

## Ejercicio 8: Autenticación

### 8.1 GitHub Token

Para obtener un token de GitHub:
1. Ve a: https://github.com/settings/tokens
2. "Generate new token" → "Personal access token (classic)"
3. Selecciona scopes: `repo`, `user`
4. Copia el token

Crea `ejercicio8_auth.py`:

```python
import httpx
import os
from typing import Dict

class GitHubAuthClient:
    """Cliente autenticado de GitHub."""

    def __init__(self, token: str):
        self.client = httpx.Client(
            base_url="https://api.github.com",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json"
            },
            timeout=10.0
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_authenticated_user(self) -> Dict:
        """Obtiene el usuario autenticado."""
        response = self.client.get("/user")
        response.raise_for_status()
        return response.json()

    def get_private_repos(self) -> list:
        """Obtiene repos privados (requiere autenticación)."""
        response = self.client.get("/user/repos", params={"type": "private"})
        response.raise_for_status()
        return response.json()

    def create_repo(self, name: str, description: str = "", private: bool = False):
        """Crea un repositorio."""
        data = {
            "name": name,
            "description": description,
            "private": private
        }
        response = self.client.post("/user/repos", json=data)
        response.raise_for_status()
        return response.json()

# Uso
if __name__ == "__main__":
    # Obtener token de variable de entorno
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print("Error: Define GITHUB_TOKEN en variables de entorno")
        print("export GITHUB_TOKEN='tu_token_aqui'")
        exit(1)

    with GitHubAuthClient(token) as gh:
        # Usuario autenticado
        user = gh.get_authenticated_user()
        print(f"Autenticado como: {user['login']}")
        print(f"Nombre: {user['name']}")
        print(f"Email: {user['email']}")
```

**Tareas:**
1. ✅ Implementa `get_rate_limit()` para ver límites de la API
2. ✅ Agrega método para crear un gist
3. ✅ Implementa `star_repo(owner, repo)` para marcar repos con estrella

---

## Proyecto Final: Analizador de Repositorios

Crea un programa que:

1. Busque repositorios por lenguaje y keyword
2. Analice las top 10 opciones
3. Para cada repo obtenga:
   - Información básica (stars, forks, issues)
   - Contributors top 5
   - Issues abiertas recientes
   - Última release
4. Genere un reporte en formato markdown

### Estructura Sugerida

```
proyecto-final/
├── src/
│   ├── __init__.py
│   ├── client.py       # Cliente de GitHub
│   ├── analyzer.py     # Lógica de análisis
│   └── report.py       # Generador de reportes
├── tests/
│   └── test_client.py
├── requirements.txt
└── main.py
```

### Requisitos

1. ✅ Usar httpx con client reutilizable
2. ✅ Timeouts configurados
3. ✅ Manejo robusto de errores
4. ✅ Reintentos con backoff
5. ✅ Logging apropiado
6. ✅ Requests async donde sea posible
7. ✅ Rate limiting (respetar límites de GitHub)
8. ✅ Caché de resultados (opcional)
9. ✅ Tests básicos

### Ejemplo de Salida

```markdown
# Análisis de Repositorios: python web framework

## 1. django/django
⭐ 75,123 | 🍴 23,456 | 📝 Issues: 234

**Top Contributors:**
1. johndoe (1,234 commits)
2. janedoe (987 commits)
...

**Issues Recientes:**
- Fix bug in admin panel (#12345)
- Add support for Python 3.12 (#12344)
...

**Última Release:** v4.2.1 (2024-01-15)
```

### Puntos Extra

- 📊 Visualización con matplotlib/plotly
- 💾 Guardar datos en SQLite
- 🔄 Comparación entre repositorios
- 📈 Análisis de tendencias (commits por mes)
- 🌐 CLI interactiva con `rich` o `click`

---

## Recursos Adicionales

### APIs Públicas para Practicar

- **JSONPlaceholder**: https://jsonplaceholder.typicode.com
- **GitHub API**: https://docs.github.com/rest
- **HTTPBin**: https://httpbin.org (testing)
- **OpenWeather**: https://openweathermap.org/api
- **REST Countries**: https://restcountries.com
- **PokéAPI**: https://pokeapi.co
- **NASA APIs**: https://api.nasa.gov

### Documentación

- httpx: https://www.python-httpx.org
- requests: https://requests.readthedocs.io
- aiohttp: https://docs.aiohttp.org

### Herramientas Útiles

- **httpie**: CLI para testing de APIs
- **Postman**: GUI para testing
- **curl**: Comando clásico para HTTP

---

## Checklist de Completitud

- [ ] Ejercicio 1: GET requests básicos
- [ ] Ejercicio 2: CRUD completo
- [ ] Ejercicio 3: Manejo de errores
- [ ] Ejercicio 4: Reintentos y backoff
- [ ] Ejercicio 5: Client reutilizable
- [ ] Ejercicio 6: Streaming
- [ ] Ejercicio 7: Async
- [ ] Ejercicio 8: Autenticación
- [ ] Proyecto Final: Analizador completo

¡Completa todos los ejercicios para dominar el consumo de APIs en Python!
