from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.income import Income
from app.models.user import User
from app.schemas.income import IncomeCreate, IncomeResponse, IncomeUpdate
from app.services.income_service import create_income, delete_income, get_income_by_id, get_incomes, update_income


income_router = APIRouter(prefix="/incomes", tags=["Incomes"])


@income_router.get("", response_model=list[IncomeResponse])
def list_incomes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Income]:
    return get_incomes(db, current_user.id)


@income_router.get("/{income_id}", response_model=IncomeResponse)
def get_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Income:
    income = get_income_by_id(db, income_id, current_user.id)
    if income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    return income


@income_router.post("", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income_endpoint(
    income_in: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Income:
    try:
        return create_income(db, current_user.id, income_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@income_router.put("/{income_id}", response_model=IncomeResponse)
def update_income_endpoint(
    income_id: int,
    income_in: IncomeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Income:
    income = get_income_by_id(db, income_id, current_user.id)
    if income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")

    try:
        return update_income(db, income, current_user.id, income_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@income_router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income_endpoint(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    income = get_income_by_id(db, income_id, current_user.id)
    if income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")

    delete_income(db, income)

