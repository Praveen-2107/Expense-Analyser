from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeUpdate


def get_incomes(db: Session, user_id: int) -> list[Income]:
    return (
        db.query(Income)
        .filter(Income.user_id == user_id)
        .order_by(Income.income_date.desc(), Income.created_at.desc())
        .all()
    )


def get_income_by_id(db: Session, income_id: int, user_id: int) -> Income | None:
    return db.query(Income).filter(Income.id == income_id, Income.user_id == user_id).first()


def get_category_for_user(db: Session, category_id: int, user_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()


def create_income(db: Session, user_id: int, income_in: IncomeCreate) -> Income:
    if income_in.category_id is not None:
        category = get_category_for_user(db, income_in.category_id, user_id)
        if category is None:
            raise ValueError("Category not found for the current user")

    income = Income(
        user_id=user_id,
        category_id=income_in.category_id,
        title=income_in.title.strip(),
        description=income_in.description.strip() if income_in.description else None,
        amount=income_in.amount,
        income_date=income_in.income_date,
        source=income_in.source.strip() if income_in.source else None,
        is_recurring=income_in.is_recurring,
    )
    db.add(income)
    db.commit()
    db.refresh(income)
    return income


def update_income(db: Session, income: Income, user_id: int, income_in: IncomeUpdate) -> Income:
    update_data = income_in.model_dump(exclude_unset=True)

    if "category_id" in update_data and update_data["category_id"] is not None:
        category = get_category_for_user(db, update_data["category_id"], user_id)
        if category is None:
            raise ValueError("Category not found for the current user")

    for field_name, field_value in update_data.items():
        if field_name in {"title", "description", "source"} and isinstance(field_value, str):
            field_value = field_value.strip() or None
        setattr(income, field_name, field_value)

    db.commit()
    db.refresh(income)
    return income


def delete_income(db: Session, income: Income) -> None:
    db.delete(income)
    db.commit()

