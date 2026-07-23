from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class IncomeBase(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    amount: Decimal = Field(gt=0)
    income_date: date
    source: str | None = Field(default=None, max_length=100)
    is_recurring: bool = False
    category_id: int | None = None


class IncomeCreate(IncomeBase):
    pass


class IncomeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    amount: Decimal | None = Field(default=None, gt=0)
    income_date: date | None = None
    source: str | None = Field(default=None, max_length=100)
    is_recurring: bool | None = None
    category_id: int | None = None


class IncomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    category_id: int | None
    title: str
    description: str | None
    amount: Decimal
    income_date: date
    source: str | None
    is_recurring: bool
    created_at: datetime
    updated_at: datetime | None

