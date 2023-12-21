"""FastAPI model serializers"""
import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    """JWT token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT token data"""

    username: str


class User(BaseModel):
    """User info"""

    username: str
    email: str | None = None
    disabled: bool = False


class UserInDB(User):
    """User info with db fields"""

    id: UUID
    hashed_password: str


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
