from fastapi import Request
from psycopg_pool import AsyncConnectionPool
from psycopg import AsyncConnection


async def get_connection(request: Request):
    pool: AsyncConnectionPool = request.app.conn_pool
    async with pool.connection() as conn:
        yield conn
