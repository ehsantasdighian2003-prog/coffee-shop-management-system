from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings.
    Values are loaded from .env file.
    """

    # =========================
    # APPLICATION
    # =========================

    APP_NAME: str = "Coffee Shop Management System"

    # =========================
    # DATABASE
    # =========================

    DATABASE_NAME: str

    DATABASE_USER: str

    DATABASE_PASSWORD: str

    DATABASE_HOST: str = "localhost"

    DATABASE_PORT: int = 5432

    # =========================
    # JWT
    # =========================

    JWT_SECRET_KEY: str

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:

        env_file = ".env"

        env_file_encoding = "utf-8"


# =========================
# SETTINGS INSTANCE
# =========================

settings = Settings()
