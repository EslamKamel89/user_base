from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import SessionMaker

from app.core.config import settings

engine = create_async_engine(
    settings.ASYNC_DATABASE_URL ,
    pool_pre_ping=True,
    future=True
)
