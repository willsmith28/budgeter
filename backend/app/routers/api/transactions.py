"""Transactions route"""
from uuid import UUID

import fastapi

from app.auth import CurrentActiveUser
from app.db import Connection
from app.db.transaction import TransactionRepository
from app.serializers import TransactionIn, TransactionOut

router = fastapi.APIRouter(prefix="/transactions", tags=["Transaction"])


@router.get("/")
async def get_all_transactions(
    conn: Connection, user: CurrentActiveUser
) -> list[TransactionOut]:
    """Get all transactions for the current user"""
    transaction_repo = TransactionRepository(conn)
    return await transaction_repo.list(user.id)


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED)
async def create_transaction(
    conn: Connection, user: CurrentActiveUser, transaction: TransactionIn
) -> TransactionOut:
    """Create new transaction"""
    transaction_repo = TransactionRepository(conn)
    model = transaction.model_dump()
    model["id"] = await transaction_repo.create(
        transaction.amount,
        transaction.date,
        transaction.merchant_id,
        transaction.category_id,
        user.id,
    )
    return model


@router.put("/{transaction_id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def edit_transaction(
    conn: Connection,
    user: CurrentActiveUser,
    transaction_id: UUID,
    transaction: TransactionIn,
):
    """Edit transaction"""
    transaction_repo = TransactionRepository(conn)
    await transaction_repo.update(
        transaction_id,
        transaction.amount,
        transaction.date,
        transaction.merchant_id,
        transaction.category_id,
        user.id,
    )


@router.delete("/{transaction_id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    conn: Connection,
    user: CurrentActiveUser,
    transaction_id: UUID,
):
    """Delete transaction"""
    transaction_repo = TransactionRepository(conn)
    await transaction_repo.delete(transaction_id, user.id)
