# alembic/env.py
from __future__ import annotations

import os
from logging.config import fileConfig

from sqlalchemy import create_engine, engine_from_config, pool

from alembic import context

# from sqlalchemy.engine import Connection


# this is the Alembic Config object, which provides access to the .ini file
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -- Application imports --
# Import your settings and your metadata (Base).
# Make sure app package is importable (run from project root or set prepend_sys_path in alembic.ini).
from app.core.config import settings
from app.db.base import \
    Base  # ensure Base is the same DeclarativeBase your models use

# IMPORT MODEL MODULES so their tables are registered on Base.metadata.
# Import only the modules that define models to avoid heavy side-effects.
# Example:
try:
    import app.users.models  # type: ignore # noqa: F401
except Exception:
    # If model import errors happen, we want them to be visible when running alembic commands
    raise

# target metadata for 'autogenerate'
target_metadata = Base.metadata

# Helper: prefer config's sqlalchemy.url, otherwise derive a sync URL from async one.
def _get_sync_url() -> str | None:
    # alembic.ini may supply a URL via sqlalchemy.url
    ini_url = config.get_main_option("sqlalchemy.url")
    if ini_url:
        return ini_url
    # fallback: try to convert your async URL to a sync driver
    async_url = getattr(settings, "ASYNC_DATABASE_URL", None)
    if not async_url:
        return None
    # Common conversion for MySQL aiomysql -> pymysql
    if "+aiomysql" in async_url:
        return async_url.replace("+aiomysql", "+pymysql")
    # Add conversions for other drivers if needed
    return async_url

# Run migrations in 'offline' mode.
def run_migrations_offline() -> None:
    url = _get_sync_url()
    if url is None:
        raise RuntimeError("No DB URL found for offline mode (set sqlalchemy.url in alembic.ini or ASYNC_DATABASE_URL in settings)")

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

# Run migrations in 'online' mode using a sync engine.
def run_migrations_online() -> None:
    # Prefer ini config if provided; engine_from_config reads config file options which is the default Alembic behavior.
    connectable = None
    ini_url = config.get_main_option("sqlalchemy.url")
    if ini_url:
        # Let Alembic engine_from_config pick up options from alembic.ini (pool args, etc.)
        connectable = engine_from_config(
            config.get_section(config.config_ini_section) or {},
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    else:
        # Fallback: create engine directly from settings (sync URL)
        sync_url = _get_sync_url()
        if sync_url is None:
            raise RuntimeError("No DB URL found for online mode (set sqlalchemy.url in alembic.ini or ASYNC_DATABASE_URL in settings)")
        connectable = create_engine(sync_url, poolclass=pool.NullPool)

    # run migrations with the connectable
    with connectable.connect() as connection:  
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
