from contextlib import asynccontextmanager

import fastapi
from psycopg_pool import AsyncConnectionPool

from app.api import router
from app.env import POSTGRES_CONNINFO


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    """Create and manage connection pool in fastapi lifecycle"""
    async with AsyncConnectionPool(POSTGRES_CONNINFO, open=False) as pool:
        app.conn_pool = pool
        yield


def app_factory():
    """Create and configure FastAPI instance"""
    app = fastapi.FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app
