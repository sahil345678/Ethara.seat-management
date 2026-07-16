# Ethara — Local Setup & Execution Guide

This document provides step-by-step instructions for setting up, validating, and running the Ethara Seat Allocation & Project Mapping System in a local development environment.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python 3.10+**
- **Node.js 20+**
- **PostgreSQL 15+**
- **Git**

---

## 1. Backend Setup (FastAPI)

The backend is a high-performance Python ASGI application utilizing FastAPI and SQLAlchemy.

### 1.1 Database Configuration
1. Open pgAdmin or your terminal `psql`.
2. Create a new database named `ethara`.
   ```sql
   CREATE DATABASE ethara;
   ```

### 1.2 Virtual Environment & Dependencies
Open a terminal in the `backend` directory:
```bash
cd backend
python -m venv venv

# Activate on Windows:
.\venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 1.3 Environment Variables
In the `backend` directory, create a `.env` file based on the `.env.example` structure:
```env
ENVIRONMENT=development
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ethara
SECRET_KEY=local_development_secret_key_123
CORS_ORIGINS=["http://localhost:5173"]
GEMINI_API_KEY=your_google_gemini_api_key  # Optional: For AI Assistant
GEMINI_MODEL=gemini-1.5-flash
```

### 1.4 Migrations & Database Seeding
Execute Alembic to generate the tables, and then run the Phase 10 Seeder to populate the database with realistic data.
```bash
# Run Alembic migrations up to the latest revision
alembic upgrade head

# Run the database seeder (generates 100 employees, 10 projects, 3 floors)
python -m scripts.seed_db
```

### 1.5 Start the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- **API Base:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`

---

## 2. Frontend Setup (React + Vite)

The frontend is a strictly typed React 19 application heavily utilizing TanStack Query for server state management.

### 2.1 Install Dependencies
Open a second terminal in the `frontend` directory:
```bash
cd frontend
npm install
```

### 2.2 Environment Variables
Create a `.env` file in the `frontend` directory:
```env
VITE_API_URL=http://localhost:8000/api/v1
```
*(Note: Vite proxies `/api` to `http://localhost:8000` via `vite.config.ts` during local development, preventing CORS issues).*

### 2.3 Start the Development Server
```bash
npm run dev
```
- **Application URL:** `http://localhost:5173`

---

## 3. Local Runtime Testing Checklist

Once both servers are running smoothly, open `http://localhost:5173` and execute this brief validation checklist:

- [ ] **Dashboard:** Verify the 6 metric cards load and display numbers. Verify the Recharts pie/bar charts render seamlessly.
- [ ] **Employees:** Verify the paginated data table renders. Test the search bar.
- [ ] **Projects:** Verify the table renders. Click a row to expand it and confirm the "Assigned Team Members" dynamically load.
- [ ] **Seats:** Verify the SeatGrid renders and the status colors correctly reflect Available (Teal), Occupied (Blue), and Reserved (Purple) states.
- [ ] **Seat Allocation:** Select an employee, skip selecting a seat, and click "Confirm". Verify the backend Proximity Algorithm successfully assigns them a seat.
- [ ] **AI Assistant:** Type "where is my seat" (or use a real seeded name like "where is John seated?"). Verify the chat bubble resolves with an accurate response.

---

## Troubleshooting

- **Database Connection Error (`psycopg2.OperationalError`)**: Double check the `DATABASE_URL` in your backend `.env` matches your postgres credentials.
- **Frontend Network Error**: Ensure the backend terminal is running on port 8000 and the Vite proxy in `vite.config.ts` is pointed to the correct target.
- **AI Fallback Triggering**: If Gemini doesn't answer naturally, ensure your `GEMINI_API_KEY` is valid. The system will automatically fallback to keyword-parsing if the API key is missing or invalid.
