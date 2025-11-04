from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.core.config import settings

engine = create_async_engine(
    settings.ASYNC_DATABASE_URL ,
    pool_pre_ping=True,
    future=True
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine , 
    class_=AsyncSession ,
    expire_on_commit=False ,
    autoflush=False,
    autocommit=False,
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
