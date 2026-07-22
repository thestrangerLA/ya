#!/usr/bin/env pwsh
# ─────────────────────────────────────────────────────────────────────────────
# Start Backend — Animal Medicine Information System
# ─────────────────────────────────────────────────────────────────────────────

$PYTHON = "C:\Temp\PyEnv\python.exe"
$BACKEND_DIR = "$PSScriptRoot\backend"

Write-Host "Animal Medicine Information System - Backend" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Check Python
if (-not (Test-Path $PYTHON)) {
    Write-Error "Python not found at $PYTHON. Please install Python 3.11."
    exit 1
}

Set-Location $BACKEND_DIR

# Check if .env exists
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example. Please review database settings." -ForegroundColor Yellow
}

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Cyan
& $PYTHON -m alembic upgrade head

if ($LASTEXITCODE -ne 0) {
    Write-Warning "Migration failed. Is PostgreSQL running?"
}

# Start server
Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "Swagger UI: http://localhost:8000/docs" -ForegroundColor Cyan
& $PYTHON -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

