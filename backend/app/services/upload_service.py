from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pandas as pd
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.bank_statement import BankStatement
from app.models.category import Category
from app.models.expense import Expense
from app.models.income import Income
from app.models.user import User


def _uploads_root() -> Path:
    root = Path(settings.uploads_dir)
    root.mkdir(parents=True, exist_ok=True)
    return root


def _user_upload_dir(user_id: int) -> Path:
    directory = _uploads_root() / f"user_{user_id}"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _safe_filename(filename: str) -> str:
    return Path(filename).name.replace(" ", "_")


def _store_upload(file_name: str, content: bytes, user_id: int) -> Path:
    upload_path = _user_upload_dir(user_id) / f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid4().hex}_{_safe_filename(file_name)}"
    upload_path.write_bytes(content)
    return upload_path


def _get_category_map(db: Session, user_id: int) -> dict[str, Category]:
    categories = db.query(Category).filter(Category.user_id == user_id).all()
    return {category.name.lower(): category for category in categories}


def _match_category(description: str, category_map: dict[str, Category]) -> Category | None:
    normalized_description = description.lower()
    keywords = {
        "food": ["restaurant", "restaurant", "grocery", "cafe", "dining", "meal", "food"],
        "transport": ["uber", "lyft", "taxi", "metro", "bus", "train", "fuel"],
        "subscriptions": ["netflix", "spotify", "subscription", "prime", "adobe"],
        "housing": ["rent", "mortgage", "landlord", "apartment"],
        "utilities": ["electric", "water", "internet", "gas", "utility"],
    }

    for category_name, terms in keywords.items():
        if any(term in normalized_description for term in terms):
            category = category_map.get(category_name)
            if category is not None:
                return category

    for category in category_map.values():
        if category.name.lower() in normalized_description:
            return category

    return None


def _normalize_columns(columns: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for column in columns:
        normalized = re.sub(r"[^a-z0-9]", "", column.lower())
        mapping[normalized] = column
    return mapping


def _pick_column(column_map: dict[str, str], candidates: list[str]) -> str | None:
    for candidate in candidates:
        normalized = re.sub(r"[^a-z0-9]", "", candidate.lower())
        if normalized in column_map:
          return column_map[normalized]
    return None


def _parse_amount(row: dict[str, object], column_map: dict[str, str]) -> tuple[Decimal, str]:
    amount_column = _pick_column(column_map, ["amount", "transaction amount", "transactionamount", "value", "net amount"])
    debit_column = _pick_column(column_map, ["debit", "withdrawal", "money out"])
    credit_column = _pick_column(column_map, ["credit", "deposit", "money in"])

    if amount_column is not None and row.get(amount_column) not in (None, ""):
        raw_amount = Decimal(str(row[amount_column]).replace(",", "").strip())
        return abs(raw_amount), "expense" if raw_amount < 0 else "income"

    if debit_column is not None and row.get(debit_column) not in (None, ""):
        raw_amount = Decimal(str(row[debit_column]).replace(",", "").strip())
        return abs(raw_amount), "expense"

    if credit_column is not None and row.get(credit_column) not in (None, ""):
        raw_amount = Decimal(str(row[credit_column]).replace(",", "").strip())
        return abs(raw_amount), "income"

    raise ValueError("Unable to determine transaction amount from the uploaded CSV")


def _parse_date_value(row: dict[str, object], column_map: dict[str, str]) -> datetime | None:
    date_column = _pick_column(
        column_map,
        ["date", "transaction date", "transactiondate", "posted date", "posteddate", "value date", "valuedate"],
    )
    if date_column is None or row.get(date_column) in (None, ""):
        return None
    parsed = pd.to_datetime(row[date_column], errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.to_pydatetime()


def _parse_description(row: dict[str, object], column_map: dict[str, str]) -> str:
    description_column = _pick_column(
        column_map,
        ["description", "details", "narration", "merchant", "memo", "payee", "remarks"],
    )
    if description_column is None:
        return "Imported transaction"
    value = row.get(description_column)
    if value in (None, ""):
        return "Imported transaction"
    return str(value).strip() or "Imported transaction"


def _save_statement_record(
    db: Session,
    user_id: int,
    file_name: str,
    file_path: Path,
    file_type: str,
    status: str,
    parsed_summary: str | None,
) -> BankStatement:
    statement = BankStatement(
        user_id=user_id,
        file_name=file_name,
        file_path=str(file_path),
        file_type=file_type,
        upload_status=status,
        parsed_summary=parsed_summary,
        processed_at=datetime.utcnow(),
    )
    db.add(statement)
    db.commit()
    db.refresh(statement)
    return statement


def import_csv_statement(db: Session, user: User, filename: str, content: bytes) -> dict[str, object]:
    stored_path = _store_upload(filename, content, user.id)
    dataframe = pd.read_csv(stored_path)
    column_map = _normalize_columns(list(dataframe.columns))
    category_map = _get_category_map(db, user.id)

    created_transactions: list[dict[str, object]] = []
    total_expenses = 0
    total_incomes = 0
    total_amount = Decimal("0")

    for _, row in dataframe.iterrows():
        row_data = row.to_dict()
        amount, entry_type = _parse_amount(row_data, column_map)
        transaction_date = _parse_date_value(row_data, column_map)
        description = _parse_description(row_data, column_map)
        category = _match_category(description, category_map)

        total_amount += amount

        transaction_record = {
            "transaction_date": transaction_date.isoformat() if transaction_date else None,
            "title": description,
            "amount": amount,
            "entry_type": entry_type,
            "category_name": category.name if category else None,
        }
        created_transactions.append(transaction_record)

        if entry_type == "expense":
            db.add(
                Expense(
                    user_id=user.id,
                    category_id=category.id if category else None,
                    title=description[:150],
                    description=description,
                    amount=amount,
                    expense_date=(transaction_date or datetime.utcnow()).date(),
                    payment_method=None,
                    merchant_name=description[:120],
                    is_recurring=False,
                )
            )
            total_expenses += 1
        else:
            db.add(
                Income(
                    user_id=user.id,
                    category_id=category.id if category else None,
                    title=description[:150],
                    description=description,
                    amount=amount,
                    income_date=(transaction_date or datetime.utcnow()).date(),
                    source=description[:100],
                    is_recurring=False,
                )
            )
            total_incomes += 1

    db.commit()

    summary = (
        f"Imported {len(created_transactions)} CSV transactions. "
        f"Created {total_expenses} expenses and {total_incomes} income records."
    )
    statement = _save_statement_record(db, user.id, filename, stored_path, "csv", "processed", summary)

    return {
        "statement": statement,
        "transactions": created_transactions,
        "imported_expenses": total_expenses,
        "imported_incomes": total_incomes,
        "total_transactions": len(created_transactions),
        "total_amount": total_amount,
        "summary": summary,
        "parser_type": "csv",
        "used_pdf_extraction": False,
    }


def import_pdf_statement(db: Session, user: User, filename: str, content: bytes) -> dict[str, object]:
    stored_path = _store_upload(filename, content, user.id)
    reader = PdfReader(str(stored_path))
    extracted_text_chunks: list[str] = []

    for page in reader.pages[:3]:
        text = page.extract_text() or ""
        if text.strip():
            extracted_text_chunks.append(text.strip())

    page_count = len(reader.pages)
    character_count = sum(len(chunk) for chunk in extracted_text_chunks)
    summary = (
        f"Uploaded PDF statement with {page_count} pages. "
        f"Extracted {character_count} characters from the first pages for review."
    )
    if extracted_text_chunks:
        summary += f" Preview: {extracted_text_chunks[0][:240]}"

    statement = _save_statement_record(db, user.id, filename, stored_path, "pdf", "processed", summary)

    return {
        "statement": statement,
        "transactions": [],
        "imported_expenses": 0,
        "imported_incomes": 0,
        "total_transactions": 0,
        "total_amount": Decimal("0"),
        "summary": summary,
        "parser_type": "pdf",
        "used_pdf_extraction": bool(extracted_text_chunks),
    }


def list_statements(db: Session, user_id: int) -> list[BankStatement]:
    return (
        db.query(BankStatement)
        .filter(BankStatement.user_id == user_id)
        .order_by(BankStatement.created_at.desc())
        .all()
    )

