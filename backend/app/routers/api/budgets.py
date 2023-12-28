"""Budget routes"""
from uuid import UUID

import fastapi

from app.auth import CurrentActiveUser
from app.db import Connection
from app.db.budget import BudgetRepository
from app.serializers import BudgetEdit, BudgetIn, BudgetOut

router = fastapi.APIRouter(prefix="/budgets")


@router.get("/")
async def get_all_budgets(conn: Connection, user: CurrentActiveUser) -> list[BudgetOut]:
    """Get all budget items for the logged in user"""
    budget_repo = BudgetRepository(conn)
    return await budget_repo.list(user.id)


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED)
async def create_budget(
    conn: Connection, user: CurrentActiveUser, budget: BudgetIn
) -> BudgetOut:
    """Create new budget item"""
    budget_repo = BudgetRepository(conn)
    model = budget.model_dump()
    model["id"] = await budget_repo.create(user_id=user.id, **model)
    return model


@router.put(
    "/{budget_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
async def edit_budget(
    budget_id: UUID,
    budget: BudgetEdit,
    user: CurrentActiveUser,
    conn: Connection,
):
    """Update amount on budget item"""
    budget_repo = BudgetRepository(conn)
    await budget_repo.update(amount=budget.amount, budget_id=budget_id, user_id=user.id)


@router.delete(
    "/{budget_id}",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
async def delete_budget(budget_id: UUID, user: CurrentActiveUser, conn: Connection):
    """Delete budget item"""
    budget_repo = BudgetRepository(conn)
    await budget_repo.delete(budget_id=budget_id, user_id=user.id)
