"""Category routes"""
import fastapi

from app.auth import get_current_active_user
from app.db import Connection
from app.db.category import CategoryRepository
from app.serializers import CategoryIn, CategoryOut

router = fastapi.APIRouter(
    prefix="/categories", dependencies=[fastapi.Depends(get_current_active_user)]
)


@router.get("/")
async def get_all_categories(conn: Connection) -> list[CategoryOut]:
    """Get all Categories"""
    category_repo = CategoryRepository(conn)
    return await category_repo.list()


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED)
async def create_category(conn: Connection, category: CategoryIn) -> CategoryOut:
    """Create new Category"""
    category_repo = CategoryRepository(conn)
    model = category.model_dump()
    model["id"] = await category_repo.create(category.name)
    return model
