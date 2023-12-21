"""User routes"""
import fastapi
from psycopg import AsyncConnection
from psycopg.errors import UniqueViolation
from app.auth import get_password_hash
from app.dependencies.db import ConnectionPool
from app.serializers import UserSignUp

router = fastapi.APIRouter(prefix="/user")


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED)
async def user_sign_up(connection_pool: ConnectionPool, user_info: UserSignUp):
    """New user sign up"""
    hashed_password = get_password_hash(user_info.password)
    user = user_info.model_dump()
    user["hashed_password"] = hashed_password
    user.pop("password")
    sql = (
        'INSERT INTO "user" (username, email, hashed_password) '
        "VALUES (%(username)s, %(email)s, %(hashed_password)s)"
    )
    conn: AsyncConnection
    try:
        async with connection_pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, user)
    except UniqueViolation as err:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail={"message": str(err)},
        ) from err
