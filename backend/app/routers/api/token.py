"""Token routes"""
from typing import Annotated
import fastapi
from fastapi.security import OAuth2PasswordRequestForm
from psycopg import AsyncConnection
from app.dependencies.db import ConnectionPool
from app.serializers import TokenResponse
from app.auth import authenticate_user, create_access_token

router = fastapi.APIRouter(prefix="/token")


@router.post("/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, fastapi.Depends()],
    connection_pool: ConnectionPool,
) -> TokenResponse:
    """Get access token"""
    conn: AsyncConnection
    async with connection_pool.connection() as conn:
        user = await authenticate_user(conn, form_data.username, form_data.password)

    if user is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Incorrect username or password"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# TODO refresh tokens
