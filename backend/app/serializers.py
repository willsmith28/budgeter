"""FastAPI model serializers"""
import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CategoryIn(BaseModel):
    """User input for Category"""

    name: str


class CategoryOut(CategoryIn):
    """Response model for Category"""

    id: UUID


class MerchantIn(BaseModel):
    """User input for Merchant"""

    name: str


class MerchantOut(MerchantIn):
    """Response model for Merchant"""

    id: UUID


class TransactionIn(BaseModel):
    """User input for Transaction"""

    amount: Decimal
    date: datetime.date
    merchant_id: UUID
    category_id: UUID


class TransactionOut(TransactionIn):
    """Response model for Transaction"""

    id: UUID


class BudgetIn(BaseModel):
    """User input for Budget"""

    amount: Decimal
    category_id: UUID


class BudgetOut(BudgetIn):
    """Response model for Budget"""

    id: UUID
