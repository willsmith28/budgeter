from fastapi import APIRouter

from app.api import category

router = APIRouter(prefix="/api")

router.include_router(category.router)
