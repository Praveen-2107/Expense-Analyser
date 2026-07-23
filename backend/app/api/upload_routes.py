from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.upload import UploadResponse, StatementResponse
from app.services.upload_service import import_csv_statement, import_pdf_statement, list_statements


upload_router = APIRouter(prefix="/uploads", tags=["Uploads"])


def _validate_file_extension(filename: str, expected_extension: str) -> None:
    if not filename.lower().endswith(expected_extension):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only {expected_extension} files are supported")


@upload_router.get("/statements", response_model=list[StatementResponse])
def get_statements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_statements(db, current_user.id)


@upload_router.post("/csv", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _validate_file_extension(file.filename or "", ".csv")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded CSV file is empty")

    result = import_csv_statement(db, current_user, file.filename or "uploaded.csv", content)
    statement = result["statement"]
    return {
        "statement_id": statement.id,
        "file_name": statement.file_name,
        "file_type": statement.file_type,
        "status": statement.upload_status,
        "parser_type": result["parser_type"],
        "summary": result["summary"],
        "total_transactions": result["total_transactions"],
        "imported_expenses": result["imported_expenses"],
        "imported_incomes": result["imported_incomes"],
        "total_amount": result["total_amount"],
        "transactions": result["transactions"],
        "used_pdf_extraction": result["used_pdf_extraction"],
    }


@upload_router.post("/pdf", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _validate_file_extension(file.filename or "", ".pdf")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded PDF file is empty")

    result = import_pdf_statement(db, current_user, file.filename or "uploaded.pdf", content)
    statement = result["statement"]
    return {
        "statement_id": statement.id,
        "file_name": statement.file_name,
        "file_type": statement.file_type,
        "status": statement.upload_status,
        "parser_type": result["parser_type"],
        "summary": result["summary"],
        "total_transactions": result["total_transactions"],
        "imported_expenses": result["imported_expenses"],
        "imported_incomes": result["imported_incomes"],
        "total_amount": result["total_amount"],
        "transactions": result["transactions"],
        "used_pdf_extraction": result["used_pdf_extraction"],
    }

