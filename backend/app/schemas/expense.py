from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    amount: Decimal = Field(gt=0)
    expense_date: date
    payment_method: str | None = Field(default=None, max_length=50)
    merchant_name: str | None = Field(default=None, max_length=120)
    is_recurring: bool = False
    category_id: int | None = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    amount: Decimal | None = Field(default=None, gt=0)
    expense_date: date | None = None
    payment_method: str | None = Field(default=None, max_length=50)
    merchant_name: str | None = Field(default=None, max_length=120)
    is_recurring: bool | None = None
    category_id: int | None = None


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    category_id: int | None
    title: str
    description: str | None
    amount: Decimal
    expense_date: date
    payment_method: str | None
    merchant_name: str | None
    is_recurring: bool
    created_at: datetime
    updated_at: datetime | None

