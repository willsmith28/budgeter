"""Merchant routes routes"""
import fastapi

from app.auth import get_current_active_user
from app.db import Connection
from app.db.merchant import MerchantRepository
from app.serializers import MerchantIn, MerchantOut

router = fastapi.APIRouter(
    prefix="/merchants", dependencies=[fastapi.Depends(get_current_active_user)]
)


@router.get("/")
async def get_all_merchants(conn: Connection) -> list[MerchantOut]:
    """get all merchants"""
    merchant_repo = MerchantRepository(conn)
    return await merchant_repo.list()


@router.post("/")
async def create_merchant(conn: Connection, merchant: MerchantIn) -> MerchantOut:
    """Create new merchant"""
    merchant_repo = MerchantRepository(conn)
    model = merchant.model_dump()
    model["id"] = await merchant_repo.create(merchant.name)
    return model
