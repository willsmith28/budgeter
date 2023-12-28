"""User routes"""
import fastapi

from app.auth import get_password_hash
from app.db import Connection
from app.db.user import UserRepository
from app.serializers import UserSignUp

router = fastapi.APIRouter(prefix="/user")


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED)
async def user_sign_up(conn: Connection, user_info: UserSignUp):
    """New user sign up"""
    hashed_password = get_password_hash(user_info.password)
    user_repo = UserRepository(conn)
    await user_repo.create(user_info.username, user_info.email, hashed_password)
    return {"message": "sign up successful. Proceed to login."}
