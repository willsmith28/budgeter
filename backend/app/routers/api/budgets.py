"""Budget routes"""
from uuid import UUID

import fastapi
from psycopg import AsyncConnection
from psycopg.errors import UniqueViolation, ForeignKeyViolation, IntegrityError
from psycopg.rows import dict_row

from app.auth import CurrentActiveUser
from app.dependencies.db import ConnectionPool
from app.serializers import BudgetIn, BudgetOut, BudgetEdit


router = fastapi.APIRouter(prefix="/budgets")


@router.get("/")
async def get_all_budgets(
    connection_pool: ConnectionPool, user: CurrentActiveUser
) -> list[BudgetOut]:
    """Get all budget items for the logged in user"""
    sql = "SELECT id, amount, category_id FROM budget WHERE user_id = %s;"
    conn: AsyncConnection
    async with connection_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(sql, (user.id,))
            return cursor.fetchall()


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED)
async def create_budget(
    connection_pool: ConnectionPool, user: CurrentActiveUser, budget: BudgetIn
) -> BudgetOut:
    """Create new budget item"""
    sql = (
        "INSERT INTO budget (amount, category_id, user_id) "
        "VALUES (%(amount)s, %(category_id)s, %(user_id)s) "
        "RETURNING id;"
    )
    budget_dict = budget.model_dump()
    budget_dict["user_id"] = user.id
    conn: AsyncConnection
    try:
        async with connection_pool.connection() as conn:
            async with conn.cursor() as cursor:
                cursor.execute(sql, budget_dict)
                result = await cursor.fetchone()
                budget_dict["id"] = result[0]

    except (UniqueViolation, ForeignKeyViolation) as err:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT, detail={"message": str(err)}
        )

    return budget_dict


@router.put(
    "/{budget_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
async def edit_budget(
    budget_id: UUID,
    budget: BudgetEdit,
    user: CurrentActiveUser,
    connection_pool: ConnectionPool,
):
    """Update amount on budget item"""
    sql = (
        "UPDATE budget SET amount = %(amount)s "
        "WHERE id = %(id)s AND user_id = %(user_id)s;"
    )
    budget_dict = budget.model_dump()
    budget_dict["id"] = budget_id
    budget_dict["user_id"] = user.id
    conn: AsyncConnection
    try:
        async with connection_pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, budget_dict)
                if cursor.rowcount == 0:
                    raise fastapi.HTTPException(
                        status_code=fastapi.status.HTTP_404_NOT_FOUND,
                        detail={
                            "message": "No budget item could be found with the provided ID"
                        },
                    )
    except IntegrityError as err:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT, detail={"message": str(err)}
        ) from err


@router.delete(
    "/{budget_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
async def delete_budget(
    budget_id: UUID, user: CurrentActiveUser, connection_pool: ConnectionPool
):
    """Delete budget item"""
    sql = "DELETE FROM budget WHERE id = %s AND user_id = %s;"
    conn: AsyncConnection
    try:
        async with connection_pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, (budget_id, user.id))
                if cursor.rowcount == 0:
                    raise fastapi.HTTPException(
                        status_code=fastapi.status.HTTP_404_NOT_FOUND,
                        detail={
                            "message": "No budget item could be found with the provided ID"
                        },
                    )
    except IntegrityError as err:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT, detail={"message": str(err)}
        )
