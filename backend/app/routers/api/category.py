"""Category routes"""
import fastapi
from psycopg import AsyncConnection
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row

from app.auth import get_current_active_user
from app.dependencies.db import ConnectionPool
from app.serializers import CategoryIn, CategoryOut

router = fastapi.APIRouter(
    prefix="/categories", dependencies=[fastapi.Depends(get_current_active_user)]
)


@router.get("/")
async def get_all_categories(conn_pool: ConnectionPool) -> list[CategoryOut]:
    """Get all Categories"""
    sql = "SELECT * FROM category"
    conn: AsyncConnection
    async with conn_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(f"{sql};")
            return await cursor.fetchall()


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED)
async def create_category(
    conn_pool: ConnectionPool, category: CategoryIn
) -> CategoryOut:
    """Create new Category"""
    sql = "INSERT INTO category (name) VALUES (%(name)s) RETURNING id;"
    category_dict = category.model_dump()
    conn: AsyncConnection
    try:
        async with conn_pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, category_dict)
                results = await cursor.fetchone()
                category_dict["id"] = results[0]

    except UniqueViolation as err:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail={"message": str(err)},
        )

    return category_dict
