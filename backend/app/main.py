"""Create and configure FastAPI application"""
from contextlib import asynccontextmanager

import fastapi
from psycopg_pool import AsyncConnectionPool

from app import routers
from app.config import POSTGRES_CONNINFO


@asynccontextmanager
async def postgres_pool_lifespan(app: fastapi.FastAPI):
    """Create and manage connection pool in fastapi lifecycle"""
    async with AsyncConnectionPool(POSTGRES_CONNINFO, open=False) as pool:
        app.conn_pool = pool
        yield


def app_factory():
    """Create and configure FastAPI instance"""
    app = fastapi.FastAPI(lifespan=postgres_pool_lifespan)
    app.include_router(routers.router)

    return app
