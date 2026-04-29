"""
Configuración de base de datos SQLAlchemy.

Proporciona engine, SessionLocal y Base para los modelos.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# Engine de SQLAlchemy
engine = create_engine(
    settings.database_url, connect_args={"check_same_thread": False}  # Solo para SQLite
)

# SessionLocal para crear sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base para modelos
class Base(DeclarativeBase):
    """Clase base para todos los modelos SQLAlchemy."""

    pass


def get_db() -> Session:
    """
    Dependencia para obtener sesión de base de datos.

    Uso:
        @app.get("/items/")
        def get_items(db: Session = Depends(get_db)):
            ...

    Yields:
        Session de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
