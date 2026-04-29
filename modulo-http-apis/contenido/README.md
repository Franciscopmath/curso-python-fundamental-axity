# Módulo 7: HTTP y Consumo de APIs

## Tabla de Contenidos

1. [Introducción a HTTP](#1-introducción-a-http)
2. [requests - Cliente HTTP Clásico](#2-requests---cliente-http-clásico)
3. [httpx - Cliente HTTP Moderno](#3-httpx---cliente-http-moderno)
4. [aiohttp - Cliente Asíncrono](#4-aiohttp---cliente-asíncrono)
5. [Timeouts y Resiliencia](#5-timeouts-y-resiliencia)
6. [Reintentos y Backoff](#6-reintentos-y-backoff)
7. [Manejo de Errores](#7-manejo-de-errores)
8. [Streaming](#8-streaming)
9. [Autenticación](#9-autenticación)
10. [Buenas Prácticas](#10-buenas-prácticas)

---

## 1. Introducción a HTTP

### Conceptos Básicos

HTTP (HyperText Transfer Protocol) es el protocolo de comunicación en la web.

**Métodos HTTP:**
- **GET**: Obtener recursos
- **POST**: Crear recursos
- **PUT**: Actualizar recursos (completo)
- **PATCH**: Actualizar recursos (parcial)
- **DELETE**: Eliminar recursos
- **HEAD**: Obtener solo encabezados
- **OPTIONS**: Obtener métodos permitidos

**Códigos de Estado:**
- **2xx**: Éxito (200 OK, 201 Created, 204 No Content)
- **3xx**: Redirección (301 Moved, 302 Found, 304 Not Modified)
- **4xx**: Error del cliente (400 Bad Request, 401 Unauthorized, 404 Not Found)
- **5xx**: Error del servidor (500 Internal Server Error, 503 Service Unavailable)

---

## 2. requests - Cliente HTTP Clásico

`requests` es la librería HTTP más popular de Python.

### Instalación

```bash
pip install requests
```

### Uso Básico

```python
import requests

# GET request
response = requests.get("https://api.github.com/users/octocat")
print(response.status_code)  # 200
print(response.json())       # Parsea JSON automáticamente

# POST request
data = {"name": "John", "email": "john@example.com"}
response = requests.post(
    "https://api.example.com/users",
    json=data  # Envía como JSON
)

# Con parámetros de query
params = {"q": "python", "sort": "stars"}
response = requests.get(
    "https://api.github.com/search/repositories",
    params=params
)
# URL: https://api.github.com/search/repositories?q=python&sort=stars
```

### Headers y Autenticación

```python
import requests

# Headers personalizados
headers = {
    "User-Agent": "MiApp/1.0",
    "Accept": "application/json"
}
response = requests.get("https://api.example.com", headers=headers)

# Autenticación básica
response = requests.get(
    "https://api.example.com/secure",
    auth=("username", "password")
)

# Bearer token
headers = {"Authorization": "Bearer YOUR_TOKEN"}
response = requests.get("https://api.example.com", headers=headers)

# API Key
headers = {"X-API-Key": "YOUR_API_KEY"}
response = requests.get("https://api.example.com", headers=headers)
```

### Timeouts

```python
import requests

# Timeout simple (segundos)
response = requests.get("https://api.example.com", timeout=5)

# Timeout separado (conexión, lectura)
response = requests.get(
    "https://api.example.com",
    timeout=(3.05, 27)  # 3.05s conectar, 27s leer
)
```

### Limitaciones de requests

- **No soporta HTTP/2**
- **No es asíncrono**
- **Sin soporte nativo de reintentos**
- **Session no es thread-safe**

---

## 3. httpx - Cliente HTTP Moderno

`httpx` es la evolución de requests con soporte HTTP/2 y async.

### Instalación

```bash
pip install httpx
```

### Ventajas sobre requests

✅ API compatible con requests
✅ Soporte HTTP/2
✅ Soporte async/await
✅ Timeouts más configurables
✅ Mejor manejo de streams
✅ Thread-safe

### Uso Básico

```python
import httpx

# Idéntico a requests
response = httpx.get("https://api.github.com/users/octocat")
print(response.status_code)
print(response.json())

# POST
data = {"name": "John"}
response = httpx.post("https://api.example.com/users", json=data)
```

### Client Reutilizable

```python
import httpx

# ✓ Recomendado: Usar Client para reutilizar conexiones
with httpx.Client() as client:
    response1 = client.get("https://api.example.com/users")
    response2 = client.get("https://api.example.com/posts")
    # Conexión HTTP reutilizada

# Headers base para todas las requests
with httpx.Client(
    base_url="https://api.example.com",
    headers={"User-Agent": "MiApp/1.0"},
    timeout=10.0
) as client:
    response = client.get("/users")  # https://api.example.com/users
```

### HTTP/2

```python
import httpx

# HTTP/2 habilitado por defecto
with httpx.Client(http2=True) as client:
    response = client.get("https://http2.github.io")
    print(response.http_version)  # HTTP/2
```

### Async/Await

```python
import httpx
import asyncio

async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

# Múltiples requests concurrentes
async def fetch_multiple():
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f"https://api.example.com/users/{i}")
            for i in range(1, 11)
        ]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

# Ejecutar
asyncio.run(fetch_multiple())
```

---

## 4. aiohttp - Cliente Asíncrono

`aiohttp` es especializado para operaciones asíncronas.

### Instalación

```bash
pip install aiohttp
```

### Uso Básico

```python
import aiohttp
import asyncio

async def fetch():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com") as response:
            return await response.json()

asyncio.run(fetch())
```

### Comparación httpx vs aiohttp

| Característica | httpx | aiohttp |
|----------------|-------|---------|
| API | Compatible con requests | Propia |
| HTTP/2 | ✓ | ✗ |
| Sync + Async | ✓ | Solo async |
| Documentación | Excelente | Buena |
| Rendimiento | Muy bueno | Excelente |

**Recomendación:** Usar `httpx` para la mayoría de casos.

---

## 5. Timeouts y Resiliencia

### Tipos de Timeout

```python
import httpx

# Timeout global (aplica a todo)
client = httpx.Client(timeout=10.0)

# Timeouts granulares
timeout = httpx.Timeout(
    connect=5.0,    # Tiempo para conectar
    read=10.0,      # Tiempo para leer respuesta
    write=5.0,      # Tiempo para escribir request
    pool=10.0       # Tiempo esperando conexión del pool
)
client = httpx.Client(timeout=timeout)

# Sin timeout (peligroso)
response = httpx.get("https://api.example.com", timeout=None)

# Timeout infinito para lectura (streaming)
timeout = httpx.Timeout(connect=5.0, read=None)
```

### Pool de Conexiones

```python
import httpx

# Configurar límites del pool
limits = httpx.Limits(
    max_connections=100,        # Conexiones totales
    max_keepalive_connections=20,  # Conexiones keep-alive
    keepalive_expiry=30.0       # Tiempo de keep-alive
)

client = httpx.Client(limits=limits)
```

---

## 6. Reintentos y Backoff

### Estrategias de Reintento

```python
import httpx
import time
from typing import Callable

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    exceptions: tuple = (httpx.RequestError, httpx.HTTPStatusError)
):
    """Reintenta una función con backoff exponencial."""
    for attempt in range(max_retries):
        try:
            return func()
        except exceptions as e:
            if attempt == max_retries - 1:
                raise

            wait_time = backoff_factor ** attempt
            print(f"Intento {attempt + 1} falló. Reintentando en {wait_time}s...")
            time.sleep(wait_time)

# Uso
def make_request():
    response = httpx.get("https://api.example.com/data", timeout=5)
    response.raise_for_status()
    return response.json()

data = retry_with_backoff(make_request)
```

### httpx-retry (extensión)

```bash
pip install httpx-retry
```

```python
from httpx_retry import RetryTransport

transport = RetryTransport(
    max_retries=3,
    backoff_factor=2.0,
    respect_retry_after_header=True
)

with httpx.Client(transport=transport) as client:
    response = client.get("https://api.example.com")
```

---

## 7. Manejo de Errores

### Excepciones de httpx

```python
import httpx

try:
    response = httpx.get("https://api.example.com", timeout=5)
    response.raise_for_status()  # Lanza excepción si 4xx o 5xx

except httpx.ConnectTimeout:
    print("Timeout al conectar")

except httpx.ReadTimeout:
    print("Timeout al leer respuesta")

except httpx.TimeoutException:
    print("Timeout general")

except httpx.NetworkError:
    print("Error de red")

except httpx.HTTPStatusError as e:
    print(f"Error HTTP: {e.response.status_code}")
    print(f"Respuesta: {e.response.text}")

except httpx.RequestError as e:
    print(f"Error en request: {e}")
```

### Verificar Código de Estado

```python
import httpx

response = httpx.get("https://api.example.com")

# Método 1: Verificar manualmente
if response.status_code == 200:
    data = response.json()
elif response.status_code == 404:
    print("No encontrado")
elif response.status_code >= 500:
    print("Error del servidor")

# Método 2: raise_for_status()
try:
    response.raise_for_status()
except httpx.HTTPStatusError as e:
    if e.response.status_code == 404:
        print("Recurso no encontrado")
    elif e.response.status_code >= 500:
        print("Error del servidor")

# Método 3: is_error, is_success
if response.is_success:  # 2xx
    data = response.json()
elif response.is_error:  # 4xx, 5xx
    print(f"Error: {response.status_code}")
```

---

## 8. Streaming

### Streaming de Descargas

```python
import httpx
from pathlib import Path

# ✓ Streaming (eficiente en memoria)
with httpx.stream("GET", "https://example.com/large-file.zip") as response:
    total_bytes = 0
    with open("file.zip", "wb") as f:
        for chunk in response.iter_bytes(chunk_size=8192):
            f.write(chunk)
            total_bytes += len(chunk)
            print(f"Descargado: {total_bytes / 1024 / 1024:.2f} MB")

# ✗ No streaming (carga todo en memoria)
response = httpx.get("https://example.com/large-file.zip")
Path("file.zip").write_bytes(response.content)  # Peligroso para archivos grandes
```

### Streaming con Client

```python
import httpx

with httpx.Client() as client:
    with client.stream("GET", "https://example.com/large.json") as response:
        # Procesar línea por línea
        for line in response.iter_lines():
            process_line(line)

# Streaming async
async with httpx.AsyncClient() as client:
    async with client.stream("GET", "https://example.com/data") as response:
        async for chunk in response.aiter_bytes():
            process_chunk(chunk)
```

### Progress Tracking

```python
import httpx
from tqdm import tqdm

url = "https://example.com/large-file.zip"

with httpx.stream("GET", url) as response:
    total_size = int(response.headers.get("content-length", 0))

    with open("file.zip", "wb") as f:
        with tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
            for chunk in response.iter_bytes(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))
```

---

## 9. Autenticación

### Bearer Token

```python
import httpx

headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}

with httpx.Client(headers=headers) as client:
    response = client.get("https://api.example.com/protected")
```

### API Key

```python
import httpx

# En header
headers = {"X-API-Key": "YOUR_API_KEY"}
client = httpx.Client(headers=headers)

# En query params
params = {"api_key": "YOUR_API_KEY"}
response = httpx.get("https://api.example.com/data", params=params)
```

### OAuth 2.0

```python
import httpx

# Obtener token
token_response = httpx.post(
    "https://oauth.example.com/token",
    data={
        "grant_type": "client_credentials",
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET"
    }
)
access_token = token_response.json()["access_token"]

# Usar token
headers = {"Authorization": f"Bearer {access_token}"}
response = httpx.get("https://api.example.com/data", headers=headers)
```

### Custom Auth

```python
import httpx

class CustomAuth(httpx.Auth):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def auth_flow(self, request):
        request.headers["X-API-Key"] = self.api_key
        yield request

auth = CustomAuth("YOUR_API_KEY")
response = httpx.get("https://api.example.com", auth=auth)
```

---

## 10. Buenas Prácticas

### 1. Usar Context Managers

```python
# ✓ Correcto
with httpx.Client() as client:
    response = client.get("https://api.example.com")

# ✗ Incorrecto
client = httpx.Client()
response = client.get("https://api.example.com")
# Falta cerrar client.close()
```

### 2. Configurar Timeouts

```python
# ✓ Siempre configurar timeout
response = httpx.get("https://api.example.com", timeout=10)

# ✗ Sin timeout (puede colgar indefinidamente)
response = httpx.get("https://api.example.com")
```

### 3. Verificar Status Code

```python
# ✓ Verificar siempre
response = httpx.get("https://api.example.com")
response.raise_for_status()

# o

if response.is_success:
    data = response.json()
```

### 4. Manejar Errores

```python
# ✓ Manejo robusto
try:
    response = httpx.get("https://api.example.com", timeout=5)
    response.raise_for_status()
    data = response.json()
except httpx.TimeoutException:
    logger.error("Timeout al conectar a la API")
except httpx.HTTPStatusError as e:
    logger.error(f"Error HTTP {e.response.status_code}")
except httpx.RequestError as e:
    logger.error(f"Error en request: {e}")
```

### 5. Reutilizar Clients

```python
# ✓ Reutilizar conexiones
with httpx.Client(base_url="https://api.example.com") as client:
    users = client.get("/users").json()
    posts = client.get("/posts").json()

# ✗ Crear cliente por request
for user_id in range(100):
    response = httpx.get(f"https://api.example.com/users/{user_id}")
```

### 6. Usar Streaming para Archivos Grandes

```python
# ✓ Streaming
with httpx.stream("GET", url) as response:
    with open("file.zip", "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)

# ✗ Cargar todo en memoria
response = httpx.get(url)
Path("file.zip").write_bytes(response.content)
```

### 7. Configurar Reintentos

```python
# ✓ Implementar reintentos
def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = httpx.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### 8. Headers Apropiados

```python
# ✓ User-Agent específico
headers = {
    "User-Agent": "MiApp/1.0 (contacto@example.com)",
    "Accept": "application/json"
}
response = httpx.get("https://api.example.com", headers=headers)
```

### 9. Logging

```python
import logging
import httpx

logger = logging.getLogger(__name__)

try:
    response = httpx.get("https://api.example.com", timeout=10)
    response.raise_for_status()
    logger.info("Request exitoso: %s", response.status_code)
except httpx.RequestError as e:
    logger.error("Error en request: %s", e)
```

---

## Resumen

- **httpx**: Cliente HTTP moderno con HTTP/2 y async
- **Timeouts**: Siempre configurar (connect, read, write, pool)
- **Reintentos**: Implementar backoff exponencial
- **Errores**: Manejar TimeoutException, HTTPStatusError, RequestError
- **Streaming**: Usar para archivos grandes
- **Client reutilizable**: Mejor rendimiento
- **Logging**: Registrar requests y errores

httpx es la mejor opción para clientes HTTP en Python moderno.
