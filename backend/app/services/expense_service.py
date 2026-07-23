from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


def get_expenses(db: Session, user_id: int) -> list[Expense]:
    return (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .order_by(Expense.expense_date.desc(), Expense.created_at.desc())
        .all()
    )


def get_expense_by_id(db: Session, expense_id: int, user_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()


def get_category_for_user(db: Session, category_id: int, user_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()


def create_expense(db: Session, user_id: int, expense_in: ExpenseCreate) -> Expense:
    if expense_in.category_id is not None:
        category = get_category_for_user(db, expense_in.category_id, user_id)
        if category is None:
            raise ValueError("Category not found for the current user")

    expense = Expense(
        user_id=user_id,
        category_id=expense_in.category_id,
        title=expense_in.title.strip(),
        description=expense_in.description.strip() if expense_in.description else None,
        amount=expense_in.amount,
        expense_date=expense_in.expense_date,
        payment_method=expense_in.payment_method.strip() if expense_in.payment_method else None,
        merchant_name=expense_in.merchant_name.strip() if expense_in.merchant_name else None,
        is_recurring=expense_in.is_recurring,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def update_expense(db: Session, expense: Expense, user_id: int, expense_in: ExpenseUpdate) -> Expense:
    update_data = expense_in.model_dump(exclude_unset=True)

    if "category_id" in update_data and update_data["category_id"] is not None:
        category = get_category_for_user(db, update_data["category_id"], user_id)
        if category is None:
            raise ValueError("Category not found for the current user")

    for field_name, field_value in update_data.items():
        if field_name in {"title", "description", "payment_method", "merchant_name"} and isinstance(field_value, str):
            field_value = field_value.strip() or None
        setattr(expense, field_name, field_value)

    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense: Expense) -> None:
    db.delete(expense)
    db.commit()

