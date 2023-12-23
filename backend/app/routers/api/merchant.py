"""Merchant routes routes"""
import fastapi
from psycopg import AsyncConnection
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row

from app.auth import get_current_active_user
from app.dependencies.db import ConnectionPool
from app.serializers import MerchantIn, MerchantOut

router = fastapi.APIRouter(
    prefix="/merchant", dependencies=[fastapi.Depends(get_current_active_user)]
)


@router.get("/")
async def get_all_merchants(connection_pool: ConnectionPool) -> list[MerchantOut]:
    """get all merchants"""
    sql = "SELECT * FROM merchant"
    conn: AsyncConnection
    async with connection_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(f"{sql};")
            return await cursor.fetchall()


@router.post("/")
async def create_merchant(
    connection_pool: ConnectionPool, merchant: MerchantIn
) -> MerchantOut:
    """Create new merchant"""
    sql = "INSERT INTO merchant (name) VALUES (%(name)s) RETURNING id;"
    merchant_dict = merchant.model_dump()
    conn: AsyncConnection
    try:
        async with connection_pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, merchant_dict)
                results = await cursor.fetchone()
                merchant_dict["id"] = results[0]

    except UniqueViolation as err:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail={
                "message": str(err),
            },
        )

    return merchant_dict
