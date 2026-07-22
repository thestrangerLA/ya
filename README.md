# 🐾 Animal Medicine Information System

A production-ready web application for managing animal medicine information, diseases, inventory, and veterinary queries.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.x (async) |
| Migrations | Alembic |
| File Storage | Local filesystem |

---

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+ (available at `C:\Temp\PyEnv\python.exe`)
- PostgreSQL 15 (or Docker)

### 1. Start PostgreSQL

Using Docker:
```bash
docker run -d \
  --name animal_medicine_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=animal_medicine_db \
  -p 5432:5432 \
  postgres:15-alpine
```

Or using Docker Compose (recommended):
```bash
docker-compose up db -d
```

### 2. Start the Backend

```bash
cd backend

# Install dependencies (Windows with custom Python path)
C:\Temp\PyEnv\python.exe -m pip install -r requirements.txt

# Run database migrations
C:\Temp\PyEnv\python.exe -m alembic upgrade head

# (Optional) Seed sample data
C:\Temp\PyEnv\python.exe seed.py

# Start the API server
C:\Temp\PyEnv\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: http://localhost:8000
Swagger UI: http://localhost:8000/docs

### 3. Start the Frontend

```bash
cd frontend

npm install
npm run dev
```

Frontend will be available at: http://localhost:3000

---

## Features

| Feature | Description |
|---|---|
| 📊 **Dashboard** | Stats overview, recent medicines, inventory alerts |
| 💊 **Medicines** | Full CRUD with image upload, filtering, sorting |
| 🦠 **Diseases** | Full CRUD with recommended medicine linking |
| 🐾 **Animal Types** | Manage 10 default animal categories |
| 🔍 **Search** | Full-text search across medicines and diseases |
| 🤖 **AI Assistant** | Symptom-based disease + medicine queries (local DB only) |
| 📦 **Inventory** | Low stock and expiration alerts |
| 🖼️ **Image Upload** | Drag-and-drop, multiple images, preview |

---

## Project Structure

```
animal-medicine-system/
├── frontend/          # Next.js app
│   ├── src/
│   │   ├── app/       # Pages (App Router)
│   │   ├── components/ # Reusable components
│   │   ├── lib/       # API client, utilities
│   │   └── types/     # TypeScript types
│   └── ...
├── backend/           # FastAPI app
│   ├── app/
│   │   ├── api/       # Route handlers
│   │   ├── core/      # Configuration
│   │   ├── crud/      # Database operations
│   │   ├── db/        # Database setup
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   └── services/  # Business logic
│   ├── alembic/       # Migrations
│   ├── uploads/       # Image storage
│   └── seed.py        # Sample data
├── docker-compose.yml
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/dashboard/stats` | Dashboard statistics |
| GET | `/api/v1/medicines/` | List medicines (paginated) |
| POST | `/api/v1/medicines/` | Create medicine |
| GET | `/api/v1/medicines/{id}` | Get medicine detail |
| PATCH | `/api/v1/medicines/{id}` | Update medicine |
| DELETE | `/api/v1/medicines/{id}` | Delete medicine |
| POST | `/api/v1/medicines/{id}/images` | Upload image |
| GET | `/api/v1/diseases/` | List diseases |
| POST | `/api/v1/diseases/` | Create disease |
| GET | `/api/v1/search/` | Full-text search |
| POST | `/api/v1/ai/query` | AI assistant query |
| GET | `/api/v1/inventory/report` | Inventory report |

Full API documentation at: http://localhost:8000/docs

---

## Environment Variables

### Backend (`.env`)
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/animal_medicine_db
UPLOAD_DIR=uploads
LOW_STOCK_THRESHOLD=10
EXPIRY_ALERT_DAYS=30
```

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Default Animal Types

Chicken, Fighting Chicken, Cattle, Pig, Goat, Sheep, Dog, Cat, Fish, Bird

## Default Medicine Categories

Antibiotic, Antiparasitic, Antiviral, Vaccine, Anti-inflammatory, Vitamin & Supplement, Antifungal, Disinfectant
