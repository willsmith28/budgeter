"""Create and configure FastAPI application"""
import fastapi

from app import routers
from app.db import postgres_pool_lifespan


def app_factory():
    """Create and configure FastAPI instance"""
    app = fastapi.FastAPI(lifespan=postgres_pool_lifespan)
    app.include_router(routers.router)

    return app
