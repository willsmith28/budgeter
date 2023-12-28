"""Routers under the /api prefix"""
import importlib
import pathlib

from fastapi import APIRouter

_current_file = pathlib.Path(__file__)

router = APIRouter(prefix="/api")

_modules = (
    importlib.import_module(f"app.routers.api.{_file.stem}")
    for _file in _current_file.parent.iterdir()
    if _file.stem != "__init__"
)

for _module in _modules:
    router.include_router(_module.router)
