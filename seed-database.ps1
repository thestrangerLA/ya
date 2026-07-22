#!/usr/bin/env pwsh
# ─────────────────────────────────────────────────────────────────────────────
# Seed Database — Animal Medicine Information System
# ─────────────────────────────────────────────────────────────────────────────

$PYTHON = "C:\Temp\PyEnv\python.exe"
$BACKEND_DIR = "$PSScriptRoot\backend"

Write-Host "🌱 Seeding database with sample data..." -ForegroundColor Green
Set-Location $BACKEND_DIR
& $PYTHON seed.py
