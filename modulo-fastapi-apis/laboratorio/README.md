# Laboratorio: APIs Web con FastAPI

API completa de gestión de pedidos con autenticación JWT, validación Pydantic y tests de integración.

## Estructura del Proyecto

```
laboratorio/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI principal
│   ├── config.py            # Configuración (Pydantic Settings)
│   ├── database.py          # SQLAlchemy setup
│   ├── dependencies.py      # Dependencias compartidas (auth)
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── user.py
│   │   └── order.py
│   ├── schemas/             # Schemas Pydantic
│   │   ├── auth.py
│   │   └── order.py
│   ├── routers/             # Routers FastAPI
│   │   ├── auth.py          # Registro y login JWT
│   │   └── orders.py        # CRUD de pedidos
│   └── utils/
│       └── security.py      # JWT y password hashing
├── tests/
│   ├── conftest.py          # Fixtures de pytest
│   ├── test_auth.py         # Tests de autenticación
│   └── test_orders.py       # Tests de CRUD
├── .env.example
├── pyproject.toml
└── README.md
```

## Instalación

```bash
cd laboratorio
poetry install
```

## Configuración

Crear archivo `.env` (copiar desde `.env.example`):

```env
DATABASE_URL=sqlite:///./orders.db
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Ejecutar la Aplicación

```bash
# Con reload automático (desarrollo)
poetry run uvicorn app.main:app --reload

# Producción
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Acceder a:
- **API**: http://localhost:8000
- **Documentación Interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación Alternativa (ReDoc)**: http://localhost:8000/redoc

## Endpoints Implementados

### Autenticación (`/auth`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Registrar nuevo usuario | No |
| POST | `/auth/token` | Login (obtener JWT) | No |
| GET | `/auth/me` | Información del usuario actual | Sí |

### Pedidos (`/orders`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/orders/` | Crear pedido | Sí |
| GET | `/orders/` | Listar pedidos del usuario | Sí |
| GET | `/orders/{id}` | Obtener pedido por ID | Sí |
| PUT | `/orders/{id}` | Actualizar pedido | Sí |
| DELETE | `/orders/{id}` | Eliminar pedido | Sí |

## Uso de la API

### 1. Registrar Usuario

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### 2. Login (Obtener Token JWT)

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=securepass123"
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 3. Crear Pedido (Requiere Auth)

```bash
TOKEN="eyJhbGciOiJIUzI1NiIs..."

curl -X POST http://localhost:8000/orders/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Laptop Dell XPS 13",
    "quantity": 2,
    "unit_price": 1299.99
  }'
```

### 4. Listar Pedidos

```bash
curl http://localhost:8000/orders/ \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Actualizar Pedido

```bash
curl -X PUT http://localhost:8000/orders/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "quantity": 3
  }'
```

### 6. Eliminar Pedido

```bash
curl -X DELETE http://localhost:8000/orders/1 \
  -H "Authorization: Bearer $TOKEN"
```

## Schemas Pydantic

### UserCreate
```python
{
  "username": str (3-50 chars),
  "email": EmailStr,
  "password": str (8+ chars)
}
```

### OrderCreate
```python
{
  "product_name": str (1-200 chars, no whitespace),
  "quantity": int (> 0, <= 10000),
  "unit_price": Decimal (> 0, 2 decimals)
}
```

### OrderUpdate
```python
{
  "product_name": Optional[str],
  "quantity": Optional[int],
  "unit_price": Optional[Decimal],
  "status": Optional["pending"|"processing"|"completed"|"cancelled"]
}
```

## Validaciones Implementadas

**User:**
- Username único, 3-50 caracteres
- Email válido y único
- Password mínimo 8 caracteres

**Order:**
- Quantity > 0 y <= 10000
- Unit price > 0
- Product name sin espacios al inicio/final
- Status: pending/processing/completed/cancelled
- Total calculado automáticamente

## Seguridad

### Autenticación JWT

- Algoritmo HS256
- Expiración configurable (default: 30 min)
- Token en header `Authorization: Bearer <token>`

### Passwords

- Hasheado con bcrypt
- Nunca se exponen en respuestas
- Validación de longitud mínima

### Autorización

- Usuarios solo pueden acceder a sus propios pedidos
- HTTP 403 si intenta acceder a pedidos de otros usuarios

## Testing

### Ejecutar Todos los Tests

```bash
poetry run pytest
```

### Tests con Coverage

```bash
poetry run pytest --cov=app --cov-report=html
```

### Tests Específicos

```bash
# Solo tests de autenticación
poetry run pytest tests/test_auth.py -v

# Solo tests de orders
poetry run pytest tests/test_orders.py -v

# Test específico
poetry run pytest tests/test_auth.py::test_register_user_success -v
```

## Cobertura de Tests

**test_auth.py (13 tests):**
- ✅ Registro de usuarios (exitoso, duplicados, validaciones)
- ✅ Login (exitoso, credenciales incorrectas)
- ✅ Obtener usuario actual (con/sin token, token inválido)

**test_orders.py (17 tests):**
- ✅ CRUD completo de pedidos
- ✅ Validaciones (cantidad, precio, nombre)
- ✅ Cálculo automático de total
- ✅ Paginación
- ✅ Autorización (usuarios no pueden ver pedidos de otros)

**Total: 30 tests**

## Características Implementadas

✅ FastAPI con estructura profesional
✅ Routers organizados por dominio
✅ Pydantic schemas con validación automática
✅ Autenticación JWT completa
✅ Registro y login de usuarios
✅ CRUD completo de pedidos
✅ Autorización (usuarios solo ven sus pedidos)
✅ Middlewares (CORS)
✅ Base de datos con SQLAlchemy
✅ Dependency injection
✅ Documentación OpenAPI automática
✅ 30 tests de integración con DB temporal
✅ Type hints completos
✅ 100% PEP 8 compliant

## Documentación Interactiva

FastAPI genera automáticamente documentación interactiva en `/docs`:

1. Ir a http://localhost:8000/docs
2. Probar endpoints directamente desde el navegador
3. Autenticarse usando el botón "Authorize"
4. Ver esquemas de request/response
5. Ver códigos de error posibles

## Mejores Prácticas Aplicadas

1. **Separación de responsabilidades**: Models, Schemas, Routers, Services
2. **Validación automática**: Pydantic valida todo
3. **Seguridad**: JWT, password hashing, autorización
4. **Testing**: Tests con DB en memoria (SQLite)
5. **Type hints**: Todo el código tipado
6. **Documentación**: OpenAPI generada automáticamente
7. **Configuración**: Variables de entorno con Pydantic Settings
8. **Dependency Injection**: Reutilización de lógica (auth, DB)

## Recursos

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Tutorial FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)

## Objetivos de Aprendizaje Cubiertos

✅ Estructura de proyecto FastAPI profesional
✅ Routers y organización de endpoints
✅ Esquemas Pydantic y validación automática
✅ Documentación OpenAPI generada
✅ Autenticación JWT (registro, login, protección)
✅ Middlewares y CORS
✅ Testing de endpoints con pytest + httpx
✅ Base de datos temporal para tests
✅ Dependency injection
✅ Response models y status codes

---

**¡La API está lista para producción!** 🚀
