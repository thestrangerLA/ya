"""
FastAPI application entry point.

Features:
    - CORS for local Next.js dev server
    - Static file serving for uploaded images
    - Lifespan: creates upload directory on startup
    - Global exception handlers
    - API v1 router
    - OpenAPI docs at /docs
"""

import os
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ── Lifespan ───────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: setup on startup, cleanup on shutdown."""
    # Ensure upload directory exists
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    (upload_path / "medicines").mkdir(exist_ok=True)
    logger.info(f"✅ Upload directory ready: {upload_path.resolve()}")
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} started")
    yield
    logger.info("🛑 Application shutting down")


# ── App Instance ───────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "REST API for the Animal Medicine Information System. "
        "Manage medicines, diseases, animal types, inventory, and AI-powered symptom queries."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ── CORS ───────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Static Files (uploaded images) ────────────────────────────────────────

upload_path = Path(settings.UPLOAD_DIR)
upload_path.mkdir(parents=True, exist_ok=True)

app.mount(
    "/api/v1/files",
    StaticFiles(directory=str(upload_path)),
    name="uploaded_files",
)


# ── API Routes ─────────────────────────────────────────────────────────────

app.include_router(api_router, prefix="/api/v1")


# ── Global Exception Handlers ──────────────────────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "success": False},
    )


# ── Health Check ───────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }
