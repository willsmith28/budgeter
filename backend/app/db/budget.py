"""Budget repository"""
from decimal import Decimal
from uuid import UUID

import fastapi
from psycopg import AsyncConnection
from psycopg.errors import IntegrityError
from psycopg.rows import dict_row

BUDGET_404 = {"message": "No budget item could be found with the provided ID"}


class BudgetRepository:
    """Budget repository. Encapsulates database access for budget objects"""

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def get(self, budget_id: UUID, user_id: UUID) -> dict:
        """Get specific budget owned by the given user"""
        sql = (
            "SELECT id, amount, category_id FROM budget "
            "WHERE id = %s AND user_id = %s;"
        )
        async with self.conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(sql, (budget_id, user_id))
            result = await cursor.fetchone()

        if result is None:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=BUDGET_404
            )

        return result

    async def list(self, user_id: UUID) -> list[dict]:
        """Get all budgets owned by the given user"""
        sql = "SELECT id, amount, category_id FROM budget WHERE user_id = %s;"
        async with self.conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(sql, (user_id,))
            return await cursor.fetchall()

    async def create(self, amount: Decimal, category_id: UUID, user_id: UUID) -> UUID:
        """Create new budget"""
        sql = (
            "INSERT INTO budget (amount, category_id, user_id) "
            "VALUES (%(amount)s, %(category_id)s, %(user_id)s) "
            "RETURNING id;"
        )
        params = {
            "amount": amount,
            "category_id": category_id,
            "user_id": user_id,
        }
        try:
            async with self.conn.transaction(), self.conn.cursor() as cursor:
                await cursor.execute(sql, params)
                result = await cursor.fetchone()
                return result[0]
        except IntegrityError as err:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_409_CONFLICT,
                detail={"message": str(err)},
            )

    async def update(self, amount: Decimal, budget_id: UUID, user_id: UUID):
        """Update a budget owned by the given user"""
        sql = (
            "UPDATE budget SET amount = %(amount)s "
            "WHERE id = %(id)s AND user_id = %(user_id)s;"
        )
        params = {
            "id": budget_id,
            "amount": amount,
            "user_id": user_id,
        }
        try:
            async with self.conn.transaction(), self.conn.cursor() as cursor:
                await cursor.execute(sql, params)
                not_found = cursor.rowcount == 0
        except IntegrityError as err:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_409_CONFLICT,
                detail={"message": str(err)},
            ) from err

        if not_found:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=BUDGET_404
            )

    async def delete(self, budget_id: UUID, user_id: UUID):
        """Delete a budget owned by the given user"""
        sql = "DELETE FROM budget WHERE id = %s AND user_id = %s;"
        async with self.conn.transaction(), self.conn.cursor() as cursor:
            await cursor.execute(sql, (budget_id, user_id))
            not_found = cursor.rowcount == 0

        if not_found:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=BUDGET_404
            )
