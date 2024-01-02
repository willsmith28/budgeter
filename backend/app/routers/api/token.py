"""Token routes"""
from typing import Annotated

import fastapi
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import authenticate_user, create_access_token
from app.db import Connection
from app.serializers import TokenResponse

router = fastapi.APIRouter(prefix="/token", tags=["Token"])


@router.post("/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, fastapi.Depends()],
    conn: Connection,
) -> TokenResponse:
    """Get access token"""
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
