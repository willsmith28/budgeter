"""FastAPI model serializers"""
import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr


class TokenResponse(BaseModel):
    """JWT token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT token data"""

    username: str


class User(BaseModel):
    """User info"""

    username: str
    email: EmailStr | None = None


class UserSignUp(User):
    """Info needed for user sign up"""

    password: str


class UserInDB(User):
    """User info with db fields"""

    id: UUID
    hashed_password: str
    disabled: bool = False


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


class BudgetEdit(BaseModel):
    """Edit model for Budget"""

    amount: Decimal


class BudgetIn(BudgetEdit):
    """User input for Budget"""

    category_id: UUID


class BudgetOut(BudgetIn):
    """Response model for Budget"""

    id: UUID
