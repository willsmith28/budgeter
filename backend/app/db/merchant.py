"""Merchant repository"""
from uuid import UUID

import fastapi
from psycopg import AsyncConnection
from psycopg.errors import IntegrityError
from psycopg.rows import dict_row

MERCHANT_404 = {"message": "No merchant could be found with the provided ID"}


class MerchantRepository:
    """Merchant repository. Encapsulates database access for merchant objects"""

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def get(self, merchant_id: UUID) -> dict:
        """Get a specific merchant"""
        sql = "SELECT * FROM merchant WHERE id = %s;"
        async with self.conn.cursor() as cursor:
            await cursor.execute(sql, (merchant_id,))
            result = await cursor.fetchone()

        if result is None:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=MERCHANT_404
            )

        return result

    async def list(self) -> list[dict]:
        """Get all categories"""
        sql = "SELECT * FROM merchant;"
        async with self.conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(sql)
            return await cursor.fetchall()

    async def create(self, name: str) -> UUID:
        """Create new merchant"""
        sql = "INSERT INTO merchant (name) VALUES (%s) RETURNING id;"
        try:
            async with self.conn.transaction(), self.conn.cursor() as cursor:
                await cursor.execute(sql, (name,))
                result = await cursor.fetchone()
                return result[0]
        except IntegrityError as err:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_409_CONFLICT,
                detail={"message": str(err)},
            )

    async def update(self, name: str, merchant_id: UUID):
        """Update a merchant"""
        sql = "UPDATE merchant SET name = %s WHERE id = %s;"

        try:
            async with self.conn.transaction(), self.conn.cursor() as cursor:
                await cursor.execute(sql, (name, merchant_id))
                not_found = cursor.rowcount == 0
        except IntegrityError as err:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_409_CONFLICT,
                detail={"message": str(err)},
            ) from err

        if not_found:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=MERCHANT_404
            )

    async def delete(self, merchant_id: UUID):
        """Delete a merchant"""
        sql = "DELETE FROM merchant WHERE id = %s;"
        async with self.conn.transaction(), self.conn.cursor() as cursor:
            await cursor.execute(sql, (merchant_id,))
            not_found = cursor.rowcount == 0

        if not_found:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=MERCHANT_404
            )
