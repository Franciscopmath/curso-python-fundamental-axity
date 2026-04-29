"""
Aplicación principal de FastAPI.

API de gestión de pedidos con autenticación JWT.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, orders

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(orders.router)


@app.get("/", tags=["root"])
def root():
    """
    Endpoint raíz de la API.

    Returns:
        Mensaje de bienvenida
    """
    return {
        "message": "Welcome to Order Management API",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Endpoint de health check.

    Returns:
        Estado del servicio
    """
    return {"status": "healthy", "service": settings.app_name}
