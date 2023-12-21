"""Contains all routers"""
import fastapi

from app.routers import api

router = fastapi.APIRouter()

router.include_router(api.router)
