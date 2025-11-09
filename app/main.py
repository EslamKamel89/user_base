from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)
        await conn.run_sync(Base.metadata.create_all)
        print('App started successfully')
        yield
        print('App stopped successfully')

def create_app()->FastAPI :
    app = FastAPI(
        title= settings.APP_NAME,
        docs_url='/docs' , 
        redoc_url='/redoc',
        lifespan=lifespan
    )
    @app.get('/health')
    async def health(): # type: ignore
        return {"status" : "ok"}
    app.include_router(users_router)
    return app

app = create_app()