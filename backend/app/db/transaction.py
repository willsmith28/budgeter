"""Transaction repository"""
import datetime
from decimal import Decimal
from uuid import UUID

import fastapi
from psycopg import AsyncConnection
from psycopg.errors import IntegrityError
from psycopg.rows import dict_row

TRANSACTION_404 = {"message": "No transaction could be found with the provided ID"}


class TransactionRepository:
    """Transaction repository. Encapsulates database access for transaction objects"""

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def get(self, transaction_id: UUID, user_id: UUID) -> dict:
        """Get a specific transaction"""
        sql = 'SELECT * FROM "transaction" WHERE id = %s AND user_id = %s'
        async with self.conn.cursor() as cursor:
            await cursor.execute(f"{sql};", (transaction_id, user_id))
            result = await cursor.fetchone()

        if result is None:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=TRANSACTION_404
            )

        return result

    async def list(
        self,
        user_id: UUID,
        prev_date: datetime.date | None = None,
        prev_id: UUID | None = None,
        limit: int = 50,
    ) -> list[dict]:
        """Get all categories"""
        conditions = ["user_id = %s"]
        params = [user_id]
        if prev_date:
            conditions.append('"date" < %s')
            params.append(prev_date)
        if prev_id:
            conditions.append("id < %s")
            params.append(prev_id)

        where_clause = " AND ".join(conditions)
        sql = f'SELECT * FROM "transaction" WHERE {where_clause} ORDER BY "date" DESC LIMIT %s;'
        params.append(limit)
        async with self.conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(sql, params)
            return await cursor.fetchall()

    async def create(
        self,
        amount: Decimal,
        date: datetime.date,
        merchant_id: UUID,
        category_id: UUID,
        user_id: UUID,
    ) -> UUID:
        """Create new transaction"""
        sql = (
            'INSERT INTO "transaction" (amount, "date", user_id, merchant_id, category_id) '
            "VALUES (%(amount)s, %(date)s, %(user_id)s, %(merchant_id)s, %(category_id)s) "
            "RETURNING id;"
        )
        params = {
            "amount": amount,
            "date": date,
            "user_id": user_id,
            "merchant_id": merchant_id,
            "category_id": category_id,
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

    async def update(
        self,
        transaction_id: UUID,
        amount: Decimal,
        date: datetime.date,
        merchant_id: UUID,
        category_id: UUID,
        user_id: UUID,
    ):
        """Update a transaction"""
        sql = (
            'UPDATE "transaction" '
            'SET amount = %(amount)s, "date" = %(date)s, '
            "category_id = %(category_id)s, merchant_id = %(merchant_id)s "
            "WHERE id = %(transaction_id)s AND user_id = %(user_id)s;"
        )
        params = {
            "transaction_id": transaction_id,
            "amount": amount,
            "date": date,
            "merchant_id": merchant_id,
            "category_id": category_id,
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
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=TRANSACTION_404
            )

    async def delete(self, transaction_id: UUID, user_id: UUID):
        """Delete a transaction"""
        sql = 'DELETE FROM "transaction" WHERE id = %s AND user_id = %s;'
        async with self.conn.transaction(), self.conn.cursor() as cursor:
            await cursor.execute(sql, (transaction_id, user_id))
            not_found = cursor.rowcount == 0

        if not_found:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=TRANSACTION_404
            )
