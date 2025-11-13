# alembic/env.py
from __future__ import annotations

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Alembic Config object
config = context.config

# Set up Python logging from alembic.ini (if defined)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    
# Import your app settings and Base metadata
from app.core.config import settings
from app.db.base import Base

print("DEBUG: Base.metadata tables:", list(Base.metadata.tables.keys()))
import app.users.models as _user_models  # type: ignore

# IMPORTANT: ensure all model modules that register tables on Base are imported.
# Import only the modules that define models (avoid heavy side-effects).
# Example:

# import app.other_app.models  # noqa: F401

# Target metadata for autogenerate
target_metadata = Base.metadata


def _get_sync_url_from_async(async_url: str) -> str:
    """
    Convert an async URL (mysql+aiomysql://...) to a sync driver (mysql+pymysql://...).
    This is used only for offline mode (rendering SQL).
    """
    if "+aiomysql" in async_url:
        return async_url.replace("+aiomysql", "+pymysql")
    # add other conversions if you use different async drivers
    return async_url


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode (no DB connection). Alembic will render SQL.
    """
    # Prefer explicit URL from alembic.ini if provided, otherwise use our app settings.
    url_from_ini = config.get_main_option("sqlalchemy.url")
    if url_from_ini:
        url = url_from_ini
    else:
        url = _get_sync_url_from_async(settings.ASYNC_DATABASE_URL)

    print("DEBUG: < offline > target_metadata tables:", target_metadata)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Run migrations using the provided (sync) connection.
    This function is executed inside connection.run_sync(...) when using the async engine.
    """
    print("DEBUG: < online > target_metadata tables:", target_metadata)
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode using an async engine.
    Create an async engine and execute the sync migration function in a sync context.
    """
    # Use NullPool to avoid connection pooling persistence during migrations
    async_engine = create_async_engine(settings.ASYNC_DATABASE_URL, poolclass=pool.NullPool)
    try:
        async with async_engine.connect() as connection:
            await connection.run_sync(do_run_migrations)
    finally:
        # Always dispose the engine to release resources
        await async_engine.dispose()


def main() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


if __name__ == "__main__":
    main()
