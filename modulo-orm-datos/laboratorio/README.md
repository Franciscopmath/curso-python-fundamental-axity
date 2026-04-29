# Laboratorio: Acceso a Datos y ORM

Este laboratorio implementa un sistema completo de gestión de pedidos utilizando SQLAlchemy ORM y migraciones con Alembic.

## Descripción del Sistema

El sistema modela una aplicación de e-commerce básica con tres entidades principales:

- **User**: Usuarios del sistema
- **Order**: Pedidos/órdenes de compra
- **OrderItem**: Items/productos dentro de cada pedido

### Diagrama de Relaciones

```
User (1) ────── (N) Order (1) ────── (N) OrderItem
```

## Estructura del Proyecto

```
laboratorio/
├── alembic/                  # Configuración y migraciones de Alembic
│   ├── versions/            # Scripts de migración
│   │   └── 001_initial_schema.py
│   ├── env.py               # Entorno de Alembic
│   ├── script.py.mako       # Template para migraciones
│   └── README
├── models.py                # Modelos SQLAlchemy (User, Order, OrderItem)
├── crud.py                  # Operaciones CRUD para todas las entidades
├── test_crud.py             # Tests con SQLite en memoria
├── alembic.ini              # Configuración de Alembic
├── pyproject.toml           # Configuración de Poetry
└── README.md                # Este archivo
```

## Requisitos

- Python 3.10 o superior
- Poetry (gestor de dependencias)

## Instalación

1. **Instalar dependencias con Poetry:**

```bash
cd laboratorio
poetry install
```

Esto instalará:
- `sqlalchemy` (ORM)
- `alembic` (migraciones)
- `pytest` (testing)
- Herramientas de desarrollo (black, mypy, ruff)

2. **Activar el entorno virtual:**

```bash
poetry shell
```

## Modelos Implementados

### User

```python
class User(Base):
    id: int (Primary Key)
    username: str (50) [unique, not null]
    email: str (100) [unique, not null]
    full_name: str (100) [not null]
    created_at: datetime [not null]

    # Relación: orders (1:N)
```

### Order

```python
class Order(Base):
    id: int (Primary Key)
    user_id: int (Foreign Key -> users.id) [not null]
    status: str (20) [not null, default='pending']
        # Valores: 'pending', 'processing', 'completed', 'cancelled'
    total: Decimal(10,2) [not null, default=0.00]
    created_at: datetime [not null]
    updated_at: datetime [not null, auto-update]

    # Relaciones:
    # - user (N:1)
    # - items (1:N, cascade delete)
```

### OrderItem

```python
class OrderItem(Base):
    id: int (Primary Key)
    order_id: int (Foreign Key -> orders.id) [not null]
    product_name: str (200) [not null]
    quantity: int [not null, default=1, > 0]
    unit_price: Decimal(10,2) [not null, >= 0]
    subtotal: Decimal(10,2) [not null, >= 0]

    # Relación: order (N:1)
```

## Operaciones CRUD Disponibles

### User CRUD

```python
from crud import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///orders.db')

with Session(engine) as session:
    # CREATE
    user = create_user(session, "johndoe", "john@example.com", "John Doe")

    # READ
    user = get_user_by_id(session, 1)
    user = get_user_by_username(session, "johndoe")
    users = get_all_users(session, limit=100)

    # UPDATE
    user = update_user(session, 1, email="newemail@example.com")

    # DELETE
    deleted = delete_user(session, 1)  # Retorna True/False
```

### Order CRUD

```python
with Session(engine) as session:
    # CREATE
    order = create_order(session, user_id=1, status="pending")

    # READ
    order = get_order_by_id(session, 1)
    orders = get_orders_by_user(session, user_id=1)
    orders = get_all_orders(session, limit=100)

    # UPDATE
    order = update_order_status(session, 1, "completed")
    order = recalculate_order_total(session, 1)

    # DELETE
    deleted = delete_order(session, 1)
```

### OrderItem CRUD

```python
from decimal import Decimal

with Session(engine) as session:
    # CREATE (agregar item a pedido)
    item = add_item_to_order(
        session,
        order_id=1,
        product_name="Laptop",
        quantity=2,
        unit_price=Decimal("999.99")
    )
    # Esto automáticamente actualiza el total del pedido

    # READ
    item = get_item_by_id(session, 1)
    items = get_items_by_order(session, order_id=1)

    # UPDATE
    item = update_item_quantity(session, item_id=1, quantity=5)
    # Recalcula subtotal y total del pedido automáticamente

    # DELETE
    deleted = delete_item(session, 1)
    # Recalcula total del pedido automáticamente
```

## Migraciones con Alembic

### Ver estado actual

```bash
alembic current
```

### Ver historial de migraciones

```bash
alembic history --verbose
```

### Aplicar migración inicial

```bash
alembic upgrade head
```

Esto creará las tablas `users`, `orders` y `order_items` en la base de datos configurada (por defecto: `orders.db`).

### Crear nueva migración (después de modificar modelos)

```bash
alembic revision --autogenerate -m "Descripción del cambio"
```

Alembic detectará automáticamente los cambios en los modelos y generará el script de migración.

### Aplicar migraciones pendientes

```bash
alembic upgrade head
```

### Revertir última migración

```bash
alembic downgrade -1
```

### Revertir todas las migraciones

```bash
alembic downgrade base
```

## Ejecutar Tests

Los tests utilizan SQLite en memoria para ser rápidos y no afectar la base de datos real.

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar con detalle verbose

```bash
pytest -v
```

### Ejecutar un test específico

```bash
pytest test_crud.py::test_create_user -v
```

### Ejecutar tests con coverage

```bash
pytest --cov=. --cov-report=html
```

## Cobertura de Tests

Los tests cubren:

- ✅ CRUD completo de User (create, read, update, delete)
- ✅ CRUD completo de Order (create, read, update, delete)
- ✅ CRUD completo de OrderItem (create, read, update, delete)
- ✅ Relaciones entre entidades
- ✅ Cascade delete (User -> Orders -> Items)
- ✅ Recálculo automático de totales
- ✅ Validaciones y constraints
- ✅ Flujo completo de creación de pedido

**Total: 21 tests**

## Ejemplo de Uso Completo

```python
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base
import crud

# Configuración
engine = create_engine('sqlite:///orders.db', echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    # 1. Crear usuario
    user = crud.create_user(
        session,
        username="alice",
        email="alice@example.com",
        full_name="Alice Wonder"
    )
    print(f"Usuario creado: {user}")

    # 2. Crear pedido
    order = crud.create_order(session, user.id)
    print(f"Pedido creado: {order}")

    # 3. Agregar items al pedido
    item1 = crud.add_item_to_order(
        session,
        order.id,
        product_name="Laptop Dell XPS 13",
        quantity=1,
        unit_price=Decimal("1299.99")
    )

    item2 = crud.add_item_to_order(
        session,
        order.id,
        product_name="Mouse Logitech MX Master 3",
        quantity=2,
        unit_price=Decimal("99.99")
    )

    # 4. Consultar pedido con total actualizado
    order = crud.get_order_by_id(session, order.id)
    print(f"Total del pedido: ${order.total}")
    # Output: Total del pedido: $1499.97

    # 5. Listar items del pedido
    items = crud.get_items_by_order(session, order.id)
    for item in items:
        print(f"- {item.product_name}: {item.quantity} x ${item.unit_price} = ${item.subtotal}")

    # 6. Actualizar estado del pedido
    crud.update_order_status(session, order.id, "processing")

    # 7. Modificar cantidad de un item
    crud.update_item_quantity(session, item1.id, 2)

    # 8. Consultar pedido actualizado
    order = crud.get_order_by_id(session, order.id)
    print(f"Total actualizado: ${order.total}")
    # Output: Total actualizado: $2799.95
```

## Validaciones Implementadas

### User
- ✅ `username` debe ser único
- ✅ `email` debe ser único
- ✅ Todos los campos requeridos no pueden ser NULL

### Order
- ✅ `status` debe ser uno de: 'pending', 'processing', 'completed', 'cancelled'
- ✅ `total` debe ser >= 0
- ✅ `user_id` debe existir en tabla users

### OrderItem
- ✅ `quantity` debe ser > 0
- ✅ `unit_price` debe ser >= 0
- ✅ `subtotal` debe ser >= 0
- ✅ `order_id` debe existir en tabla orders

## Características Avanzadas

### 1. Cascade Delete

Al eliminar un usuario, todos sus pedidos e items se eliminan automáticamente:

```python
crud.delete_user(session, user_id)
# Elimina: User + Orders + OrderItems
```

### 2. Recálculo Automático de Totales

Al agregar, modificar o eliminar items, el total del pedido se actualiza automáticamente.

### 3. Eager Loading de Relaciones

Las funciones de lectura utilizan `selectinload` para optimizar consultas y evitar el problema N+1.

### 4. Type Hints Completos

Todo el código utiliza type hints de Python 3.10+ para mejor autocompletado y detección de errores.

### 5. Timestamps Automáticos

- `created_at`: Se establece automáticamente al crear
- `updated_at`: Se actualiza automáticamente en cada modificación

## Herramientas de Desarrollo

### Formateo de código con Black

```bash
poetry run black .
```

### Verificación de tipos con MyPy

```bash
poetry run mypy models.py crud.py
```

### Linting con Ruff

```bash
poetry run ruff check .
```

## Configuración de Base de Datos

Por defecto, el laboratorio usa SQLite (`orders.db`). Para usar otra base de datos:

### PostgreSQL

Editar `alembic.ini`:

```ini
sqlalchemy.url = postgresql://user:password@localhost/dbname
```

Instalar driver:

```bash
poetry add psycopg2-binary
```

### MySQL

Editar `alembic.ini`:

```ini
sqlalchemy.url = mysql+pymysql://user:password@localhost/dbname
```

Instalar driver:

```bash
poetry add pymysql
```

## Resolución de Problemas

### Error: "No such table"

Ejecutar las migraciones:

```bash
alembic upgrade head
```

### Error: "Integrity constraint violation"

Verificar que:
- Los `user_id` y `order_id` existan antes de crear registros relacionados
- No se inserten usernames o emails duplicados

### Tests fallan

Asegurarse de tener todas las dependencias:

```bash
poetry install
```

## Recursos Adicionales

- [Documentación SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentación Alembic](https://alembic.sqlalchemy.org/)
- [Tutorial SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [Guía de Migraciones Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

## Objetivos de Aprendizaje Cubiertos

✅ Modelar entidades y relaciones en ORM (User, Order, OrderItem)
✅ Implementar CRUD básico para todas las entidades
✅ Gestionar migraciones con Alembic
✅ Configurar transacciones y sesiones
✅ Realizar pruebas con SQLite en memoria
✅ Aplicar constraints y validaciones
✅ Implementar cascade deletes
✅ Optimizar consultas con eager loading

## Licencia

Este laboratorio es material educativo para el curso de Python.
