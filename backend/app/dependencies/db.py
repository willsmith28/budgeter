"""Database related dependencies."""
from typing import Annotated

import fastapi
import psycopg_pool


def get_connection_pool(request: fastapi.Request):
    """
    Get the connection pool from the app instance. The pool itself is provided so
    transactions can be handled appropriately in the route.
    """
    yield request.app.conn_pool


ConnectionPool = Annotated[
    psycopg_pool.AsyncConnectionPool, fastapi.Depends(get_connection_pool)
]
