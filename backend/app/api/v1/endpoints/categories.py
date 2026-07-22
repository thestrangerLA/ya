"""
Category API endpoints.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_category
from app.db.database import get_db
from app.schemas.schemas import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    MessageResponse,
    PaginatedResponse,
    PaginationMeta,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=PaginatedResponse[CategoryRead])
async def list_categories(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=100, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    skip = (page - 1) * page_size
    items, total = await crud_category.get_categories(db, skip=skip, limit=page_size)
    enriched = []
    for item in items:
        count = await crud_category.get_category_medicine_count(db, item.id)
        enriched.append(
            CategoryRead(
                id=item.id, name=item.name, description=item.description,
                created_at=item.created_at, updated_at=item.updated_at,
                medicine_count=count,
            )
        )
    total_pages = max(1, -(-total // page_size))
    return PaginatedResponse(
        data=enriched,
        meta=PaginationMeta(total=total, page=page, page_size=page_size, total_pages=total_pages),
    )


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    existing = await crud_category.get_category_by_name(db, data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category '{data.name}' already exists.",
        )
    item = await crud_category.create_category(db, data)
    return CategoryRead(
        id=item.id, name=item.name, description=item.description,
        created_at=item.created_at, updated_at=item.updated_at, medicine_count=0,
    )


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    item = await crud_category.get_category(db, category_id)
    if not item:
        raise HTTPException(status_code=404, detail="Category not found.")
    count = await crud_category.get_category_medicine_count(db, category_id)
    return CategoryRead(
        id=item.id, name=item.name, description=item.description,
        created_at=item.created_at, updated_at=item.updated_at, medicine_count=count,
    )


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: uuid.UUID,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    item = await crud_category.get_category(db, category_id)
    if not item:
        raise HTTPException(status_code=404, detail="Category not found.")
    updated = await crud_category.update_category(db, item, data)
    count = await crud_category.get_category_medicine_count(db, category_id)
    return CategoryRead(
        id=updated.id, name=updated.name, description=updated.description,
        created_at=updated.created_at, updated_at=updated.updated_at, medicine_count=count,
    )


@router.delete("/{category_id}", response_model=MessageResponse)
async def delete_category(
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    item = await crud_category.get_category(db, category_id)
    if not item:
        raise HTTPException(status_code=404, detail="Category not found.")
    await crud_category.delete_category(db, item)
    return MessageResponse(message=f"Category '{item.name}' deleted successfully.")
