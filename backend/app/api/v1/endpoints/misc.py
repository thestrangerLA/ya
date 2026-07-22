"""
Dashboard, Search, AI Assistant, and Inventory endpoints.
"""

import uuid
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.crud import crud_disease, crud_medicine
from app.crud.crud_animal_type import get_animal_types
from app.db.database import get_db
from app.models.models import AnimalType, Disease, Medicine, MedicineImage
from app.schemas.schemas import (
    AIQuery,
    AIResponse,
    DashboardStats,
    ExpiringItem,
    InventoryReport,
    LowStockItem,
    MedicineListRead,
    PaginatedResponse,
    PaginationMeta,
    RecentMedicine,
    SearchResult,
)
from app.services.ai_service import ai_search

# ── Dashboard ──────────────────────────────────────────────────────────────
dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@dashboard_router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    med_stats = await crud_medicine.get_medicine_stats(db)
    disease_count = await crud_disease.get_disease_count(db)
    _, animal_count = await get_animal_types(db, limit=1000)

    return DashboardStats(
        total_medicines=med_stats["total"],
        total_diseases=disease_count,
        total_animal_types=animal_count,
        low_stock_count=med_stats["low_stock"],
        expiring_soon_count=med_stats["expiring_soon"],
    )


@dashboard_router.get("/recent-medicines", response_model=list[RecentMedicine])
async def get_recent_medicines(
    request: Request,
    limit: int = Query(default=5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    medicines = await crud_medicine.get_recent_medicines(db, limit=limit)
    result = []
    for med in medicines:
        primary_url = None
        if med.images:
            primary = next((img for img in med.images if img.is_primary), med.images[0])
            primary_url = f"{str(request.base_url).rstrip('/')}/api/v1/files/{primary.file_path}"
        result.append(
            RecentMedicine(
                id=med.id, name=med.name, brand=med.brand,
                stock_quantity=med.stock_quantity, created_at=med.created_at,
                primary_image_url=primary_url,
                animal_type_name=med.animal_type.name if med.animal_type else None,
            )
        )
    return result


# ── Search ─────────────────────────────────────────────────────────────────
search_router = APIRouter(prefix="/search", tags=["Search"])


@search_router.get("/", response_model=SearchResult)
async def search(
    request: Request,
    query: str = Query(..., min_length=1),
    animal_type_id: Optional[uuid.UUID] = Query(default=None),
    category_id: Optional[uuid.UUID] = Query(default=None),
    search_type: str = Query(default="all", pattern="^(medicine|disease|all)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
):
    skip = (page - 1) * page_size
    base_url = str(request.base_url).rstrip("/")

    medicine_results = []
    disease_results = []
    total_medicines = 0
    total_diseases = 0

    if search_type in ("medicine", "all"):
        meds, total_medicines = await crud_medicine.get_medicines(
            db, skip=skip, limit=page_size,
            animal_type_id=animal_type_id, category_id=category_id,
            search=query, sort_by=sort_by, sort_order=sort_order,
        )
        for med in meds:
            primary_url = None
            if med.images:
                p = next((img for img in med.images if img.is_primary), med.images[0])
                primary_url = f"{base_url}/api/v1/files/{p.file_path}"
            medicine_results.append(
                MedicineListRead(
                    id=med.id, name=med.name, brand=med.brand, sku=med.sku,
                    stock_quantity=med.stock_quantity, price=med.price,
                    expiration_date=med.expiration_date, created_at=med.created_at,
                    animal_type=med.animal_type, category=med.category,
                    primary_image_url=primary_url,
                )
            )

    if search_type in ("disease", "all"):
        diseases, total_diseases = await crud_disease.get_diseases(
            db, skip=skip, limit=page_size,
            animal_type_id=animal_type_id, search=query,
        )
        from app.schemas.schemas import DiseaseListRead
        disease_results = [
            DiseaseListRead(
                id=d.id, name=d.name, symptoms=d.symptoms, created_at=d.created_at,
                animal_type=d.animal_type, medicine_count=len(d.recommended_medicines),
            )
            for d in diseases
        ]

    return SearchResult(
        medicines=medicine_results,
        diseases=disease_results,
        total_medicines=total_medicines,
        total_diseases=total_diseases,
        query=query,
    )


# ── AI Assistant ───────────────────────────────────────────────────────────
ai_router = APIRouter(prefix="/ai", tags=["AI Assistant"])


@ai_router.post("/query", response_model=AIResponse)
async def ai_assistant_query(
    data: AIQuery,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    base_url = str(request.base_url).rstrip("/")
    return await ai_search(db, query=data.query, animal_type_id=data.animal_type_id, base_url=base_url)


# ── Inventory ──────────────────────────────────────────────────────────────
inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])


@inventory_router.get("/report", response_model=InventoryReport)
async def get_inventory_report(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    base_url = str(request.base_url).rstrip("/")

    low_stock_meds = await crud_medicine.get_low_stock_medicines(db)
    expiring_meds = await crud_medicine.get_expiring_medicines(db)

    # Total stock value
    value_result = await db.execute(
        select(func.sum(Medicine.price * Medicine.stock_quantity)).select_from(Medicine)
    )
    total_value = value_result.scalar_one_or_none()

    low_stock_items = []
    for med in low_stock_meds:
        primary_url = None
        if med.images:
            p = next((img for img in med.images if img.is_primary), med.images[0])
            primary_url = f"{base_url}/api/v1/files/{p.file_path}"
        low_stock_items.append(
            LowStockItem(
                id=med.id, name=med.name, brand=med.brand,
                stock_quantity=med.stock_quantity, primary_image_url=primary_url,
                animal_type_name=med.animal_type.name if med.animal_type else None,
            )
        )

    expiring_items = []
    today = date.today()
    for med in expiring_meds:
        if not med.expiration_date:
            continue
        days_until = (med.expiration_date - today).days
        primary_url = None
        if med.images:
            p = next((img for img in med.images if img.is_primary), med.images[0])
            primary_url = f"{base_url}/api/v1/files/{p.file_path}"
        expiring_items.append(
            ExpiringItem(
                id=med.id, name=med.name, brand=med.brand,
                expiration_date=med.expiration_date,
                stock_quantity=med.stock_quantity,
                days_until_expiry=days_until,
                primary_image_url=primary_url,
            )
        )

    return InventoryReport(
        low_stock_items=low_stock_items,
        expiring_items=expiring_items,
        total_low_stock=len(low_stock_items),
        total_expiring=len(expiring_items),
        total_stock_value=total_value,
    )
