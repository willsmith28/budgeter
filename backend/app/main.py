from contextlib import asynccontextmanager

import fastapi
from psycopg_pool import AsyncConnectionPool

from .env import POSTGRES_CONNINFO


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    with AsyncConnectionPool(POSTGRES_CONNINFO, open=False) as pool:
        app.conn_pool = pool
        yield


def app_factory():
    app = fastapi.FastAPI(lifespan=lifespan)
    return app


app = app_factory()


@app.get("/")
def hello_world():
    return "hello world"
