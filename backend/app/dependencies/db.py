"""Database related dependencies."""
from typing import Annotated

from fastapi import Depends, Request
from psycopg_pool import AsyncConnectionPool


def get_connection_pool(request: Request):
    """
    Get the connection pool from the app instance.
    The pool itself is provided so transactions can be handled appropriately in the route.
    """
    yield request.app.conn_pool


ConnectionPool = Annotated[AsyncConnectionPool, Depends(get_connection_pool)]
