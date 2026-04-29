"""
Configuración de la aplicación usando Pydantic Settings.

Variables de entorno se cargan desde .env o environment.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    # Información de la aplicación
    app_name: str = "Order Management API"
    app_version: str = "1.0.0"
    app_description: str = "API para gestión de pedidos con autenticación JWT"

    # Base de datos
    database_url: str = "sqlite:///./orders.db"

    # Seguridad JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Configuración
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Instancia global de configuración
settings = Settings()
