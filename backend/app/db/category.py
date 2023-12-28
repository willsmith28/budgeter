"""Category repository"""
from uuid import UUID

import fastapi
from psycopg import AsyncConnection
from psycopg.errors import IntegrityError
from psycopg.rows import dict_row

CATEGORY_404 = {"message": "No category could be found with the provided ID"}


class CategoryRepository:
    """Category repository. Encapsulates database access for category objects"""

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def get(self, category_id: UUID) -> dict:
        """Get a specific category"""
        sql = "SELECT * FROM category WHERE id = %s"
        async with self.conn.cursor() as cursor:
            await cursor.execute(f"{sql};", (category_id,))
            result = await cursor.fetchone()

        if result is None:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=CATEGORY_404
            )

        return result

    async def list(self) -> list[dict]:
        """Get all categories"""
        sql = "SELECT * FROM category;"
        async with self.conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(sql)
            return await cursor.fetchall()

    async def create(self, name: str) -> UUID:
        """Create new category"""
        sql = "INSERT INTO category (name) VALUES (%s) RETURNING id;"
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

    async def update(self, name: str, category_id: UUID):
        """Update a category"""
        sql = "UPDATE category SET name = %s WHERE id = %s;"

        try:
            async with self.conn.transaction(), self.conn.cursor() as cursor:
                await cursor.execute(sql, (name, category_id))
                not_found = cursor.rowcount == 0
        except IntegrityError as err:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_409_CONFLICT,
                detail={"message": str(err)},
            ) from err

        if not_found:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=CATEGORY_404
            )

    async def delete(self, category_id: UUID):
        """Delete a category"""
        sql = "DELETE FROM category WHERE id = %s;"
        async with self.conn.transaction(), self.conn.cursor() as cursor:
            await cursor.execute(sql, (category_id,))
            not_found = cursor.rowcount == 0

        if not_found:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=CATEGORY_404
            )
