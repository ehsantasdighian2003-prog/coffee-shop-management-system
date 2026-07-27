from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.core.config import settings

# Alembic Config object
config = context.config


# Configure database URL from application settings
config.set_main_option(
    "sqlalchemy.url",
    (
        f"postgresql+psycopg2://"
        f"{settings.DATABASE_USER}:"
        f"{settings.DATABASE_PASSWORD}@"
        f"{settings.DATABASE_HOST}:"
        f"{settings.DATABASE_PORT}/"
        f"{settings.DATABASE_NAME}"
    ),
)


# Configure Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Metadata for Alembic autogenerate
# Import your Base metadata here if needed
# Example:
# from app.models.base import Base
# target_metadata = Base.metadata

target_metadata = None


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.

    Generates SQL scripts without creating a database connection.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in online mode.

    Creates a database connection and applies migrations.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
