"""User repository"""
import fastapi
from psycopg import AsyncConnection
from psycopg.errors import IntegrityError
from psycopg.rows import dict_row

USER_404 = {"message": "No user could be found with the provided ID"}


class UserRepository:
    """User repository. Encapsulates database access for user objects"""

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def get(self, username: str) -> dict:
        """Get a specific user"""
        sql = 'SELECT * FROM "user" WHERE username = %s;'
        async with self.conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(f"{sql};", (username,))
            return await cursor.fetchone()

    async def create(self, username: str, email: str, hashed_password: str):
        """Create new user"""
        sql = (
            'INSERT INTO "user" (username, email, hashed_password) '
            "VALUES (%(username)s, %(email)s, %(hashed_password)s)"
        )
        params = {
            "username": username,
            "email": email,
            "hashed_password": hashed_password,
        }
        try:
            async with self.conn.transaction(), self.conn.cursor() as cursor:
                await cursor.execute(sql, params)
        except IntegrityError as err:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_409_CONFLICT,
                detail={"message": str(err)},
            )

    async def update(self, username: str, hashed_password: str):
        """Update a user"""
        sql = "UPDATE user SET hashed_password = %s WHERE username = %s;"

        try:
            async with self.conn.transaction(), self.conn.cursor() as cursor:
                await cursor.execute(sql, (hashed_password, username))
                not_found = cursor.rowcount == 0
        except IntegrityError as err:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_409_CONFLICT,
                detail={"message": str(err)},
            ) from err

        if not_found:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=USER_404
            )

    async def delete(self, username: str):
        """Delete a user"""
        sql = 'UPDATE user SET "disabled" = true WHERE username = %s AND "disabled" = false;'
        async with self.conn.transaction(), self.conn.cursor() as cursor:
            await cursor.execute(sql, (username,))
            not_found = cursor.rowcount == 0

        if not_found:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=USER_404
            )
