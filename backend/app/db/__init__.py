"""Database related dependencies."""
from contextlib import asynccontextmanager
from typing import Annotated, TypeAlias

import fastapi
import psycopg
import psycopg_pool

from app.config import POSTGRES_CONNINFO


@asynccontextmanager
async def postgres_pool_lifespan(app: fastapi.FastAPI):
    """Create and manage connection pool in fastapi lifecycle"""
    async with psycopg_pool.AsyncConnectionPool(
        POSTGRES_CONNINFO, kwargs={"autocommit": True}, open=False
    ) as pool:
        app.conn_pool = pool
        yield


def get_connection(request: fastapi.Request):
    """
    Get the connection pool from the app instance. The pool itself is provided so
    transactions can be handled appropriately in the route.
    """
    conn_pool: psycopg_pool.AsyncConnectionPool = request.app.conn_pool
    with conn_pool.connection() as conn:
        yield conn


Connection: TypeAlias = Annotated[
    psycopg.AsyncConnection, fastapi.Depends(get_connection)
]
