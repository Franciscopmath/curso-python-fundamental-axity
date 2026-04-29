# Módulo 9: APIs Web con FastAPI

## Introducción

FastAPI es un framework web moderno y de alto rendimiento para construir APIs con Python 3.7+ basado en type hints. Es uno de los frameworks más rápidos disponibles, comparable a NodeJS y Go, gracias a su uso de Starlette y Pydantic.

En este módulo exploraremos:
- Estructura de proyectos FastAPI profesionales
- Routers y organización de endpoints
- Validación automática con Pydantic
- Autenticación JWT
- Middlewares y CORS
- Testing de APIs con pytest

---

## 1. ¿Por Qué FastAPI?

### Ventajas Principales

1. **Alto Rendimiento**: Basado en Starlette (ASGI) y Pydantic
2. **Validación Automática**: Type hints → validación automática de datos
3. **Documentación Automática**: OpenAPI (Swagger UI) y ReDoc generados automáticamente
4. **Editor Support**: Autocompletado completo gracias a type hints
5. **Async/Await Nativo**: Soporte completo para programación asíncrona
6. **Menos Código**: Reduce código duplicado y boilerplate
7. **Production-Ready**: Usado por Microsoft, Uber, Netflix

### Comparación con Otros Frameworks

| Característica | FastAPI | Flask | Django |
|----------------|---------|-------|--------|
| Performance | ⚡⚡⚡ | ⚡ | ⚡⚡ |
| Async Support | ✅ Nativo | ❌ No | ⚠️ Desde 3.1 |
| Type Hints | ✅ Requerido | ❌ Opcional | ❌ Opcional |
| Validación | ✅ Automática | ❌ Manual | ✅ Forms/ORM |
| Docs Automáticas | ✅ OpenAPI | ❌ No | ❌ No |
| Curva Aprendizaje | Media | Baja | Alta |
| ORM Incluido | ❌ No | ❌ No | ✅ Sí |

---

## 2. Instalación y Primer Endpoint

### Instalación

```bash
pip install fastapi uvicorn[standard]
```

- `fastapi`: El framework
- `uvicorn`: Servidor ASGI de alto rendimiento

### Hello World

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

**Ejecutar:**

```bash
uvicorn main:app --reload
```

Acceder a:
- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs
- Documentación alternativa: http://localhost:8000/redoc

### Path Parameters

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

FastAPI valida automáticamente que `item_id` sea un entero.

### Query Parameters

```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

Acceso: `GET /items/?skip=5&limit=20`

---

## 3. Pydantic Schemas y Validación

### Definir Schemas

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Permite crear desde ORM models
```

### Usar Schemas en Endpoints

```python
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    # user ya está validado automáticamente
    # Aquí iría la lógica de creación en DB
    return {"id": 1, "username": user.username, "email": user.email}
```

### Validaciones Avanzadas

```python
from pydantic import BaseModel, validator, Field
from datetime import datetime

class OrderCreate(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., gt=0, le=1000)
    unit_price: float = Field(..., gt=0)

    @validator('product_name')
    def validate_product_name(cls, v):
        if v.strip() != v:
            raise ValueError('No leading/trailing whitespace allowed')
        return v

    @validator('quantity')
    def validate_quantity(cls, v):
        if v % 1 != 0:
            raise ValueError('Quantity must be an integer')
        return v
```

### Beneficios de Pydantic

✅ Validación automática de tipos
✅ Conversión automática de tipos
✅ Mensajes de error claros y detallados
✅ Serialización/deserialización JSON automática
✅ Documentación OpenAPI generada automáticamente

---

## 4. Estructura de Proyecto Profesional

### Organización Recomendada

```
proyecto/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada, app FastAPI
│   ├── config.py            # Configuración (variables de entorno)
│   ├── dependencies.py      # Dependencias compartidas
│   ├── database.py          # Configuración de base de datos
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── order.py
│   ├── schemas/             # Schemas Pydantic
│   │   ├── __init__.py
│   │   ├── order.py
│   │   └── auth.py
│   ├── routers/             # Routers (endpoints organizados)
│   │   ├── __init__.py
│   │   ├── orders.py
│   │   └── auth.py
│   ├── services/            # Lógica de negocio
│   │   ├── __init__.py
│   │   └── order_service.py
│   └── utils/               # Utilidades
│       ├── __init__.py
│       └── security.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures de pytest
│   └── test_orders.py
├── .env                     # Variables de entorno
├── pyproject.toml           # Dependencias (Poetry)
└── README.md
```

### Ventajas de Esta Estructura

1. **Separación de Responsabilidades**: Cada capa tiene una función clara
2. **Escalabilidad**: Fácil agregar nuevos módulos
3. **Testabilidad**: Componentes desacoplados facilitan testing
4. **Mantenibilidad**: Código organizado y fácil de navegar

---

## 5. Routers y Organización de Endpoints

### Crear un Router

**app/routers/orders.py:**

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter(
    prefix="/orders",
    tags=["orders"],  # Organiza documentación
)

@router.get("/", response_model=List[OrderResponse])
def get_orders(skip: int = 0, limit: int = 100):
    """Obtiene lista de pedidos."""
    return []

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate):
    """Crea un nuevo pedido."""
    return {}

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    """Obtiene un pedido específico."""
    if order_id not in database:
        raise HTTPException(status_code=404, detail="Order not found")
    return database[order_id]

@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int):
    """Elimina un pedido."""
    if order_id not in database:
        raise HTTPException(status_code=404, detail="Order not found")
    del database[order_id]
```

### Incluir Router en la App Principal

**app/main.py:**

```python
from fastapi import FastAPI
from app.routers import orders, auth

app = FastAPI(
    title="Order Management API",
    description="API para gestión de pedidos",
    version="1.0.0"
)

app.include_router(orders.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Order Management API"}
```

### Tags y Documentación

Los `tags` organizan automáticamente los endpoints en la documentación Swagger:

```python
router = APIRouter(
    prefix="/api/v1/orders",
    tags=["orders", "v1"],
    responses={404: {"description": "Not found"}},
)
```

---

## 6. Dependencias (Dependency Injection)

### Concepto

FastAPI tiene un sistema poderoso de inyección de dependencias para:
- Reutilizar lógica común
- Compartir conexiones de base de datos
- Implementar autenticación
- Validar permisos

### Dependencia Simple

```python
from fastapi import Depends

def get_query_parameters(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
def read_items(params: dict = Depends(get_query_parameters)):
    return params
```

### Dependencia de Base de Datos

```python
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/orders/")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders
```

### Dependencias Anidadas

```python
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@app.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

---

## 7. Autenticación JWT

### ¿Qué es JWT?

JSON Web Token (JWT) es un estándar abierto (RFC 7519) para transmitir información de forma segura entre partes como un objeto JSON.

**Estructura de un JWT:**
```
header.payload.signature
```

Ejemplo:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### Implementación con FastAPI

**Instalación:**

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

**Utilidades de seguridad:**

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key-keep-it-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
```

**Endpoint de Login:**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

**Proteger Endpoints:**

```python
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}
```

---

## 8. Middlewares

### ¿Qué son los Middlewares?

Middlewares son funciones que se ejecutan antes y/o después de cada request. Útiles para:
- Logging
- Autenticación
- Medición de tiempos
- Modificar headers
- Manejo de errores

### Middleware Personalizado

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Middleware de Logging

```python
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

---

## 9. CORS (Cross-Origin Resource Sharing)

### ¿Por Qué CORS?

CORS permite que tu API sea consumida desde navegadores web en dominios diferentes.

### Configuración Básica

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Configuración de Producción

```python
origins = [
    "https://miapp.com",
    "https://app.miapp.com",
    "http://localhost:3000",  # Frontend en desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

---

## 10. Manejo de Errores

### HTTPException

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in database:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Custom header"},
        )
    return database[item_id]
```

### Exception Handlers Personalizados

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse

class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"Item {exc.item_id} not found"},
    )

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in database:
        raise ItemNotFoundException(item_id)
    return database[item_id]
```

---

## 11. Testing de APIs con Pytest

### TestClient

FastAPI proporciona `TestClient` basado en `requests`:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### Tests con Base de Datos Temporal

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def test_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_create_order(client):
    response = client.post(
        "/orders/",
        json={"product_name": "Laptop", "quantity": 2, "unit_price": 999.99}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == "Laptop"
    assert "id" in data
```

### Tests de Autenticación

```python
def test_login(client):
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_endpoint_without_token(client):
    response = client.get("/protected")
    assert response.status_code == 401

def test_protected_endpoint_with_token(client):
    # Login
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass"}
    )
    token = login_response.json()["access_token"]

    # Acceder a endpoint protegido
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

---

## 12. Variables de Entorno y Configuración

### Usar Pydantic Settings

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Order API"
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

**.env:**

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Uso:**

```python
from app.config import settings

engine = create_engine(settings.database_url)
```

---

## 13. Mejores Prácticas

### 1. Versionado de API

```python
app.include_router(orders_v1.router, prefix="/api/v1")
app.include_router(orders_v2.router, prefix="/api/v2")
```

### 2. Response Models

Siempre define `response_model` para:
- Documentación clara
- Validación de respuestas
- Evitar exponer datos sensibles

```python
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    # Aunque el ORM model tenga 'password', no se expondrá
    return db.query(User).filter(User.id == user_id).first()
```

### 3. Status Codes Apropiados

```python
@app.post("/orders/", status_code=status.HTTP_201_CREATED)
@app.delete("/orders/{id}", status_code=status.HTTP_204_NO_CONTENT)
@app.get("/orders/{id}", status_code=status.HTTP_200_OK)
```

### 4. Paginación

```python
from typing import List

@app.get("/orders/", response_model=List[OrderResponse])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders
```

### 5. Documentación

```python
@app.post("/orders/", response_model=OrderResponse, status_code=201,
          summary="Create a new order",
          description="Create a new order with product details",
          response_description="The created order")
def create_order(order: OrderCreate):
    """
    Create an order with the following information:

    - **product_name**: Name of the product
    - **quantity**: Quantity ordered (must be positive)
    - **unit_price**: Price per unit
    """
    pass
```

---

## 14. Despliegue

### Uvicorn en Producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Gunicorn + Uvicorn Workers

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 15. Recursos Adicionales

**Documentación Oficial:**
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- Uvicorn: https://www.uvicorn.org/
- Starlette: https://www.starlette.io/

**Tutoriales:**
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- Full Stack FastAPI Template: https://github.com/tiangolo/full-stack-fastapi-postgresql

**Libros:**
- "Building Data Science Applications with FastAPI" - François Voron

---

## Conclusión

FastAPI es una excelente elección para construir APIs modernas en Python gracias a:

✅ Alto rendimiento (comparable a Node.js y Go)
✅ Validación automática con Pydantic
✅ Documentación interactiva automática
✅ Type hints para mejor developer experience
✅ Soporte async/await nativo
✅ Fácil de testear
✅ Production-ready desde el inicio

En el laboratorio construiremos una API completa con CRUD de pedidos, autenticación JWT, y tests de integración aplicando todos estos conceptos.
