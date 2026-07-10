import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    # =========================
    # DATABASE
    # =========================

    DATABASE_NAME = os.getenv(
        "DATABASE_NAME"
    )

    DATABASE_USER = os.getenv(
        "DATABASE_USER"
    )

    DATABASE_PASSWORD = os.getenv(
        "DATABASE_PASSWORD"
    )

    DATABASE_HOST = os.getenv(
        "DATABASE_HOST"
    )

    DATABASE_PORT = os.getenv(
        "DATABASE_PORT"
    )


    # =========================
    # JWT
    # =========================

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY"
    )

    JWT_ALGORITHM = os.getenv(
        "JWT_ALGORITHM"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            60
        )
    )


settings = Settings()