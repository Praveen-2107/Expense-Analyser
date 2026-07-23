# AI Expense Analyzer

AI Expense Analyzer is a production-oriented personal finance assistant for tracking income and expenses, analyzing spending behavior, and generating intelligent budgeting suggestions.

## Current Status

Step 1 is the initialization layer only. This repository now contains the root setup, the React + TypeScript frontend shell, and the FastAPI + SQLAlchemy backend shell.

## Folder Layout

- `frontend/` - React application scaffold with TypeScript, Tailwind CSS, Bootstrap, React Router, and Axios.
- `backend/` - FastAPI application scaffold with SQLAlchemy, Pydantic settings, and a PostgreSQL-ready database configuration.
- `.env.example` - Shared example environment variables for both applications.

## Local Development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Next Steps

The next module will be authentication with JWT login and registration.
