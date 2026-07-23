from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class UploadTransactionResponse(BaseModel):
    transaction_date: datetime | None = None
    title: str
    amount: Decimal
    entry_type: str
    category_name: str | None = None


class UploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    statement_id: int
    file_name: str
    file_type: str
    status: str
    parser_type: str
    summary: str
    total_transactions: int
    imported_expenses: int
    imported_incomes: int
    total_amount: Decimal
    transactions: list[UploadTransactionResponse] = Field(default_factory=list)
    used_pdf_extraction: bool = False


class StatementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_name: str
    file_type: str
    upload_status: str
    parsed_summary: str | None
    created_at: datetime
    processed_at: datetime | None

