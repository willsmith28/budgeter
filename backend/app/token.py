"""JWT auth support"""
import datetime
from typing import Annotated

import fastapi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from psycopg import AsyncConnection
from psycopg.rows import dict_row

from app.auth import get_password_hash, verify_password
from app.config import SECRET_KEY
from app.dependencies.db import ConnectionPool
from app.serializers import TokenData, UserInDB

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = fastapi.APIRouter()


async def get_user(conn: AsyncConnection, username: str) -> UserInDB | None:
    """Get user from database if username exists"""
    sql = "SELECT * FROM user WHERE username = %s;"
    async with conn.cursor(row_factory=dict_row) as cursor:
        await cursor.execute(sql, (username,))
        result = await cursor.fetchone()

    return UserInDB(**result) if result else None


async def authenticate_user(
    conn: AsyncConnection, username: str, password: str
) -> UserInDB | None:
    """Authenticate username and password with db"""
    user = await get_user(conn, username)
    if (
        user is None
        or user.disabled
        or not verify_password(password, user.hashed_password)
    ):
        return None

    return user


def create_access_token(
    data: dict, expires_delta: datetime.timedelta | None = None
) -> str:
    """Creates access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, fastapi.Depends(oauth2_scheme)],
    connection_pool: ConnectionPool,
) -> UserInDB:
    """Gets and verifies user info from JWT"""
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail={"message": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=(ALGORITHM,))
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError as err:
        raise credentials_exception from err

    conn: AsyncConnection
    async with connection_pool.connection() as conn:
        user = await get_user(conn, token_data.username)

    if user is None:
        raise credentials_exception

    return user


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, fastapi.Depends()],
    connection_pool: ConnectionPool,
):
    """"""
