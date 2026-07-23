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

## Docker Deployment

This repository now includes Dockerfiles for both applications and a `docker-compose.yml` file for local production-style deployment.

### Run with Docker Compose

```bash
docker compose up --build
```

### Services

- Frontend: `http://localhost`
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

### Production Notes

- Set `SECRET_KEY` to a strong random value before deploying.
- Provide `GEMINI_API_KEY` only if you want live Gemini insights.
- Update `VITE_API_BASE_URL` and `CORS_ORIGINS` to match your real domain in production.
- The backend creates the uploads directory automatically on startup.
