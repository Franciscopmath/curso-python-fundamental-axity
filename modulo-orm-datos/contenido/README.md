# Módulo 8: Acceso a Datos y ORM

## Introducción

El acceso a datos es fundamental en aplicaciones modernas. Python ofrece múltiples alternativas para trabajar con bases de datos relacionales y NoSQL, desde APIs de bajo nivel hasta ORMs completos que abstraen las operaciones SQL.

En este módulo exploraremos:
- Drivers nativos para diferentes bases de datos
- SQLAlchemy Core y ORM
- Migraciones con Alembic
- Introducción a MongoDB con Motor

---

## 1. Drivers de Bases de Datos

### 1.1 sqlite3 (Librería Estándar)

SQLite es una base de datos embebida que no requiere servidor. Python incluye `sqlite3` en su librería estándar.

**Características:**
- Sin configuración ni instalación externa
- Ideal para desarrollo, testing y aplicaciones pequeñas
- Soporta transacciones ACID
- Archivo único `.db`

**Ejemplo básico:**

```python
import sqlite3

# Conexión a base de datos (crea el archivo si no existe)
conn = sqlite3.connect('ejemplo.db')
cursor = conn.cursor()

# Crear tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
''')

# Insertar datos
cursor.execute(
    "INSERT INTO usuarios (nombre, email) VALUES (?, ?)",
    ("Juan Pérez", "juan@ejemplo.com")
)

# Commit y cierre
conn.commit()
conn.close()
```

**Gestión de contexto (recomendado):**

```python
with sqlite3.connect('ejemplo.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    resultados = cursor.fetchall()
    # El commit se hace automáticamente si no hay excepciones
```

### 1.2 psycopg2/psycopg3 (PostgreSQL)

PostgreSQL es una base de datos relacional robusta y de código abierto.

**Instalación:**
```bash
pip install psycopg2-binary  # Versión binaria
# o
pip install psycopg  # psycopg3 (versión moderna)
```

**Conexión:**

```python
import psycopg2

# Conexión a PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mi_db",
    user="usuario",
    password="contraseña"
)

cursor = conn.cursor()

# Operaciones similares a sqlite3
cursor.execute("SELECT version();")
version = cursor.fetchone()
print(f"PostgreSQL versión: {version}")

conn.close()
```

**Características avanzadas:**
- Soporte para JSON, arrays, tipos personalizados
- Transacciones robustas
- Índices avanzados (GiST, GIN, BRIN)
- Extensiones (PostGIS, pg_trgm, etc.)

### 1.3 pyodbc (SQL Server)

Para conectarse a Microsoft SQL Server se utiliza ODBC.

**Instalación:**
```bash
pip install pyodbc
```

**Conexión:**

```python
import pyodbc

# String de conexión
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=mi_db;"
    "UID=usuario;"
    "PWD=contraseña"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("SELECT @@VERSION")
version = cursor.fetchone()
print(f"SQL Server: {version}")

conn.close()
```

**Notas:**
- Requiere driver ODBC instalado en el sistema
- Compatible con Azure SQL Database
- Soporta autenticación Windows y SQL Server

---

## 2. SQLAlchemy

SQLAlchemy es el ORM más popular y completo de Python. Ofrece dos niveles de abstracción:

1. **SQLAlchemy Core**: API de expresiones SQL (bajo nivel)
2. **SQLAlchemy ORM**: Mapeo objeto-relacional (alto nivel)

### 2.1 Instalación

```bash
pip install sqlalchemy
```

### 2.2 SQLAlchemy Core

Construcción de consultas SQL mediante expresiones Python.

```python
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select

# Motor de base de datos
engine = create_engine('sqlite:///ejemplo.db', echo=True)

# Metadata y definición de tabla
metadata = MetaData()

usuarios = Table(
    'usuarios',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nombre', String(100)),
    Column('email', String(100), unique=True)
)

# Crear tablas
metadata.create_all(engine)

# Inserción
with engine.connect() as conn:
    stmt = usuarios.insert().values(nombre="Ana", email="ana@ejemplo.com")
    conn.execute(stmt)
    conn.commit()

# Consulta
with engine.connect() as conn:
    stmt = select(usuarios).where(usuarios.c.nombre == "Ana")
    result = conn.execute(stmt)
    for row in result:
        print(f"ID: {row.id}, Nombre: {row.nombre}")
```

**Ventajas de Core:**
- Control fino sobre las consultas
- Rendimiento cercano a SQL nativo
- Construcción dinámica de queries

### 2.3 SQLAlchemy ORM

Mapea clases Python a tablas de base de datos.

**Definición de modelos (estilo declarativo):**

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relación uno a muchos
    pedidos = relationship("Pedido", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(nombre='{self.nombre}', email='{self.email}')>"


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    descripcion = Column(String(200))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))

    # Relación muchos a uno
    usuario = relationship("Usuario", back_populates="pedidos")


# Crear tablas
engine = create_engine('sqlite:///orm_ejemplo.db')
Base.metadata.create_all(engine)
```

**Operaciones CRUD:**

```python
# CREATE
session = Session(engine)

nuevo_usuario = Usuario(nombre="Carlos", email="carlos@ejemplo.com")
session.add(nuevo_usuario)
session.commit()

# READ
usuario = session.query(Usuario).filter_by(email="carlos@ejemplo.com").first()
print(usuario)

# UPDATE
usuario.nombre = "Carlos Actualizado"
session.commit()

# DELETE
session.delete(usuario)
session.commit()

session.close()
```

**Consultas avanzadas:**

```python
from sqlalchemy import and_, or_, func

# Filtros complejos
usuarios = session.query(Usuario).filter(
    and_(
        Usuario.nombre.like('%Carlos%'),
        Usuario.id > 10
    )
).all()

# Joins
resultados = session.query(Usuario, Pedido).join(Pedido).filter(
    Pedido.descripcion.contains('producto')
).all()

# Agregaciones
total_usuarios = session.query(func.count(Usuario.id)).scalar()

# Ordenamiento y paginación
usuarios_paginados = session.query(Usuario)\
    .order_by(Usuario.nombre)\
    .limit(10)\
    .offset(20)\
    .all()
```

### 2.4 Relaciones en SQLAlchemy

**Uno a Muchos (One-to-Many):**

```python
class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    libros = relationship("Libro", back_populates="autor")


class Libro(Base):
    __tablename__ = 'libros'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200))
    autor_id = Column(Integer, ForeignKey('autores.id'))

    autor = relationship("Autor", back_populates="libros")
```

**Muchos a Muchos (Many-to-Many):**

```python
from sqlalchemy import Table

# Tabla de asociación
estudiante_curso = Table(
    'estudiante_curso',
    Base.metadata,
    Column('estudiante_id', Integer, ForeignKey('estudiantes.id')),
    Column('curso_id', Integer, ForeignKey('cursos.id'))
)

class Estudiante(Base):
    __tablename__ = 'estudiantes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    cursos = relationship("Curso", secondary=estudiante_curso, back_populates="estudiantes")


class Curso(Base):
    __tablename__ = 'cursos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    estudiantes = relationship("Estudiante", secondary=estudiante_curso, back_populates="cursos")
```

**Uno a Uno (One-to-One):**

```python
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    perfil = relationship("Perfil", uselist=False, back_populates="usuario")


class Perfil(Base):
    __tablename__ = 'perfiles'
    id = Column(Integer, primary_key=True)
    biografia = Column(String(500))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), unique=True)

    usuario = relationship("Usuario", back_populates="perfil")
```

### 2.5 Transacciones y Sesiones

```python
from sqlalchemy.orm import sessionmaker

# Configuración de sesión
Session = sessionmaker(bind=engine)

# Uso con context manager (recomendado)
with Session() as session:
    try:
        usuario1 = Usuario(nombre="User1", email="user1@ejemplo.com")
        usuario2 = Usuario(nombre="User2", email="user2@ejemplo.com")

        session.add_all([usuario1, usuario2])
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
```

**Patrón de sesión por request (web apps):**

```python
from contextlib import contextmanager

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Uso
with get_session() as session:
    usuario = Usuario(nombre="Test", email="test@ejemplo.com")
    session.add(usuario)
```

---

## 3. Migraciones con Alembic

Alembic es la herramienta estándar para gestionar migraciones de esquema en SQLAlchemy.

### 3.1 Instalación y Configuración

```bash
pip install alembic
```

**Inicializar Alembic:**

```bash
alembic init alembic
```

Esto crea:
- Carpeta `alembic/` con scripts de migración
- Archivo `alembic.ini` (configuración)
- Archivo `alembic/env.py` (entorno de ejecución)

**Configurar `alembic.ini`:**

```ini
sqlalchemy.url = sqlite:///./mi_base.db
# o para PostgreSQL:
# sqlalchemy.url = postgresql://user:password@localhost/dbname
```

**Configurar `alembic/env.py` (importar modelos):**

```python
from mi_app.models import Base
target_metadata = Base.metadata
```

### 3.2 Crear Migraciones

**Migración automática (detecta cambios en modelos):**

```bash
alembic revision --autogenerate -m "Crear tabla usuarios"
```

**Migración manual:**

```bash
alembic revision -m "Agregar columna telefono"
```

Editar el archivo generado en `alembic/versions/`:

```python
def upgrade():
    op.add_column('usuarios', sa.Column('telefono', sa.String(20)))

def downgrade():
    op.drop_column('usuarios', 'telefono')
```

### 3.3 Aplicar y Revertir Migraciones

```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar hasta una revisión específica
alembic upgrade ae1027a6acf

# Revertir una migración
alembic downgrade -1

# Revertir todas las migraciones
alembic downgrade base

# Ver historial
alembic history

# Ver estado actual
alembic current
```

### 3.4 Ejemplo de Migración Completa

**1. Modelo inicial:**

```python
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
```

**2. Crear migración inicial:**

```bash
alembic revision --autogenerate -m "Crear tabla usuarios"
alembic upgrade head
```

**3. Modificar modelo (agregar campo):**

```python
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    email = Column(String(100), unique=True)  # Nueva columna
```

**4. Crear y aplicar migración:**

```bash
alembic revision --autogenerate -m "Agregar email a usuarios"
alembic upgrade head
```

### 3.5 Mejores Prácticas con Alembic

1. **Siempre revisar migraciones autogeneradas** antes de aplicarlas
2. **No editar migraciones ya aplicadas** en producción
3. **Usar nombres descriptivos** para las migraciones
4. **Probar rollback** en desarrollo antes de producción
5. **Versionar migraciones** junto con el código (Git)
6. **Usar transacciones** para operaciones críticas

---

## 4. Introducción a MongoDB con Motor

### 4.1 ¿Qué es MongoDB?

MongoDB es una base de datos NoSQL orientada a documentos.

**Características:**
- Documentos JSON (BSON internamente)
- Esquema flexible
- Escalabilidad horizontal
- Consultas ricas y agregaciones
- Ideal para datos no estructurados o semi-estructurados

**Diferencias con SQL:**

| SQL                    | MongoDB              |
|------------------------|----------------------|
| Tabla                  | Colección            |
| Fila                   | Documento            |
| Columna                | Campo                |
| JOIN                   | Documentos embebidos o referencias |
| PRIMARY KEY            | _id (automático)     |

### 4.2 Motor: Cliente Async para MongoDB

**Motor** es el driver asíncrono oficial de MongoDB para Python (basado en PyMongo).

**Instalación:**

```bash
pip install motor
```

**Conexión básica:**

```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    # Conectar a MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['mi_base_datos']
    coleccion = db['usuarios']

    # Insertar documento
    resultado = await coleccion.insert_one({
        'nombre': 'María',
        'email': 'maria@ejemplo.com',
        'edad': 28
    })
    print(f"ID insertado: {resultado.inserted_id}")

    # Buscar documento
    usuario = await coleccion.find_one({'nombre': 'María'})
    print(f"Usuario encontrado: {usuario}")

    # Cerrar conexión
    client.close()

# Ejecutar
asyncio.run(main())
```

### 4.3 Operaciones CRUD con Motor

**Create (Insertar):**

```python
# Insertar uno
await coleccion.insert_one({'nombre': 'Juan', 'edad': 30})

# Insertar muchos
await coleccion.insert_many([
    {'nombre': 'Ana', 'edad': 25},
    {'nombre': 'Pedro', 'edad': 35}
])
```

**Read (Consultar):**

```python
# Buscar uno
usuario = await coleccion.find_one({'nombre': 'Juan'})

# Buscar todos (cursor)
async for usuario in coleccion.find({'edad': {'$gte': 25}}):
    print(usuario)

# Buscar con límite
usuarios = await coleccion.find().limit(10).to_list(length=10)
```

**Update (Actualizar):**

```python
# Actualizar uno
await coleccion.update_one(
    {'nombre': 'Juan'},
    {'$set': {'edad': 31}}
)

# Actualizar muchos
await coleccion.update_many(
    {'edad': {'$lt': 30}},
    {'$inc': {'edad': 1}}  # Incrementar edad en 1
)
```

**Delete (Eliminar):**

```python
# Eliminar uno
await coleccion.delete_one({'nombre': 'Juan'})

# Eliminar muchos
await coleccion.delete_many({'edad': {'$gte': 60}})
```

### 4.4 Consultas Avanzadas

**Operadores de comparación:**

```python
# Mayor que, menor que
await coleccion.find({'edad': {'$gt': 30, '$lt': 50}})

# En lista
await coleccion.find({'nombre': {'$in': ['Juan', 'Ana', 'Pedro']}})

# Expresión regular
await coleccion.find({'email': {'$regex': '.*@gmail\.com$'}})
```

**Agregaciones:**

```python
pipeline = [
    {'$match': {'edad': {'$gte': 25}}},
    {'$group': {
        '_id': '$ciudad',
        'promedio_edad': {'$avg': '$edad'},
        'total': {'$sum': 1}
    }},
    {'$sort': {'total': -1}}
]

async for resultado in coleccion.aggregate(pipeline):
    print(resultado)
```

### 4.5 Modelado de Datos

**Documentos embebidos (relación 1:N):**

```python
usuario = {
    'nombre': 'Carlos',
    'email': 'carlos@ejemplo.com',
    'direcciones': [
        {'calle': 'Av. Principal 123', 'ciudad': 'Lima'},
        {'calle': 'Jr. Secundario 456', 'ciudad': 'Cusco'}
    ]
}
```

**Referencias (relación N:M o datos grandes):**

```python
# Colección usuarios
usuario = {
    '_id': ObjectId('...'),
    'nombre': 'Carlos'
}

# Colección pedidos
pedido = {
    'usuario_id': ObjectId('...'),  # Referencia
    'productos': [...],
    'total': 150.00
}
```

### 4.6 Cuándo Usar MongoDB

**Casos de uso ideales:**
- Datos no estructurados o semi-estructurados
- Esquema que evoluciona rápidamente
- Grandes volúmenes de escrituras
- Aplicaciones en tiempo real (logs, analytics)
- Catálogos de productos (e-commerce)

**Cuándo preferir SQL:**
- Transacciones ACID complejas
- Relaciones bien definidas y normalizadas
- Consultas con múltiples JOINs
- Reportes complejos

---

## 5. Comparación de Tecnologías

| Característica        | sqlite3          | SQLAlchemy ORM    | MongoDB (Motor)   |
|-----------------------|------------------|-------------------|-------------------|
| Tipo                  | Relacional       | Relacional (ORM)  | NoSQL (Documentos)|
| Complejidad           | Baja             | Media-Alta        | Media             |
| Transacciones         | Sí               | Sí                | Limitadas         |
| Esquema               | Rígido           | Rígido            | Flexible          |
| Relaciones            | SQL nativo       | Pythonic          | Embebido/Refs     |
| Escalabilidad         | Limitada         | Depende del motor | Alta (horizontal) |
| Curva de aprendizaje  | Baja             | Media             | Media             |
| Uso recomendado       | Dev/Testing      | Producción SQL    | Big Data/NoSQL    |

---

## 6. Mejores Prácticas

### 6.1 Seguridad

1. **Nunca concatenar strings para SQL** (usar parámetros):

```python
# MAL ❌
cursor.execute(f"SELECT * FROM usuarios WHERE nombre = '{nombre}'")

# BIEN ✅
cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
```

2. **Usar variables de entorno** para credenciales:

```python
import os
from sqlalchemy import create_engine

db_url = os.getenv('DATABASE_URL', 'sqlite:///default.db')
engine = create_engine(db_url)
```

3. **Validar y sanitizar entrada de usuario**

### 6.2 Rendimiento

1. **Usar índices apropiados**:

```python
class Usuario(Base):
    __tablename__ = 'usuarios'
    email = Column(String(100), unique=True, index=True)  # Índice
```

2. **Cargar relaciones eficientemente** (evitar N+1):

```python
# Eager loading
usuarios = session.query(Usuario).options(joinedload(Usuario.pedidos)).all()
```

3. **Usar paginación** para grandes datasets

4. **Conexión pool** para aplicaciones concurrentes:

```python
engine = create_engine('postgresql://...', pool_size=10, max_overflow=20)
```

### 6.3 Mantenimiento

1. **Versionado de esquema** con Alembic
2. **Backups periódicos** de bases de datos
3. **Logging de queries** en desarrollo (no en producción)
4. **Monitoreo de rendimiento** de consultas lentas

---

## 7. Recursos Adicionales

**Documentación oficial:**
- SQLAlchemy: https://docs.sqlalchemy.org/
- Alembic: https://alembic.sqlalchemy.org/
- Motor: https://motor.readthedocs.io/
- MongoDB: https://www.mongodb.com/docs/

**Tutoriales:**
- SQLAlchemy ORM Tutorial: https://docs.sqlalchemy.org/en/20/orm/tutorial.html
- Alembic Tutorial: https://alembic.sqlalchemy.org/en/latest/tutorial.html

**Libros recomendados:**
- "Essential SQLAlchemy" - Jason Myers & Rick Copeland
- "MongoDB: The Definitive Guide" - Shannon Bradshaw

---

## Conclusión

Este módulo cubrió las herramientas esenciales para acceso a datos en Python:

- **Drivers nativos** (sqlite3, psycopg2, pyodbc) para control fino
- **SQLAlchemy ORM** para desarrollo productivo con bases relacionales
- **Alembic** para gestión profesional de migraciones
- **Motor** para trabajar con MongoDB de forma asíncrona

La elección de tecnología depende de:
- Tipo de datos (estructurado vs. no estructurado)
- Requerimientos de transacciones
- Escalabilidad necesaria
- Familiaridad del equipo

En el laboratorio aplicaremos estos conceptos creando un sistema completo con SQLAlchemy ORM y Alembic.
