#!/usr/bin/env pwsh
# ─────────────────────────────────────────────────────────────────────────────
# Start Frontend — Animal Medicine Information System
# ─────────────────────────────────────────────────────────────────────────────

$FRONTEND_DIR = "$PSScriptRoot\frontend"

Write-Host "Animal Medicine Information System - Frontend" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

Set-Location $FRONTEND_DIR

# Check if .env.local exists
if (-not (Test-Path ".env.local")) {
    @"
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Animal Medicine Information System
"@ | Out-File ".env.local" -Encoding utf8
    Write-Host "Created .env.local" -ForegroundColor Cyan
}

Write-Host "Starting Next.js on http://localhost:3000" -ForegroundColor Green
npx next dev

