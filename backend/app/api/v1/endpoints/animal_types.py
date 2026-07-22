"""
AnimalType API endpoints.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_animal_type
from app.db.database import get_db
from app.schemas.schemas import (
    AnimalTypeCreate,
    AnimalTypeRead,
    AnimalTypeUpdate,
    MessageResponse,
    PaginatedResponse,
    PaginationMeta,
)

router = APIRouter(prefix="/animal-types", tags=["Animal Types"])


@router.get("/", response_model=PaginatedResponse[AnimalTypeRead])
async def list_animal_types(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=100, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    skip = (page - 1) * page_size
    items, total = await crud_animal_type.get_animal_types(db, skip=skip, limit=page_size)

    enriched = []
    for item in items:
        counts = await crud_animal_type.get_animal_type_counts(db, item.id)
        enriched.append(
            AnimalTypeRead(
                id=item.id,
                name=item.name,
                description=item.description,
                icon=item.icon,
                created_at=item.created_at,
                updated_at=item.updated_at,
                medicine_count=counts["medicine_count"],
                disease_count=counts["disease_count"],
            )
        )

    total_pages = max(1, -(-total // page_size))
    return PaginatedResponse(
        data=enriched,
        meta=PaginationMeta(total=total, page=page, page_size=page_size, total_pages=total_pages),
    )


@router.post("/", response_model=AnimalTypeRead, status_code=status.HTTP_201_CREATED)
async def create_animal_type(
    data: AnimalTypeCreate,
    db: AsyncSession = Depends(get_db),
):
    existing = await crud_animal_type.get_animal_type_by_name(db, data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Animal type '{data.name}' already exists.",
        )
    item = await crud_animal_type.create_animal_type(db, data)
    return AnimalTypeRead(
        id=item.id, name=item.name, description=item.description, icon=item.icon,
        created_at=item.created_at, updated_at=item.updated_at,
        medicine_count=0, disease_count=0,
    )


@router.get("/{animal_type_id}", response_model=AnimalTypeRead)
async def get_animal_type(
    animal_type_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    item = await crud_animal_type.get_animal_type(db, animal_type_id)
    if not item:
        raise HTTPException(status_code=404, detail="Animal type not found.")
    counts = await crud_animal_type.get_animal_type_counts(db, animal_type_id)
    return AnimalTypeRead(
        id=item.id, name=item.name, description=item.description, icon=item.icon,
        created_at=item.created_at, updated_at=item.updated_at, **counts,
    )


@router.patch("/{animal_type_id}", response_model=AnimalTypeRead)
async def update_animal_type(
    animal_type_id: uuid.UUID,
    data: AnimalTypeUpdate,
    db: AsyncSession = Depends(get_db),
):
    item = await crud_animal_type.get_animal_type(db, animal_type_id)
    if not item:
        raise HTTPException(status_code=404, detail="Animal type not found.")
    updated = await crud_animal_type.update_animal_type(db, item, data)
    counts = await crud_animal_type.get_animal_type_counts(db, animal_type_id)
    return AnimalTypeRead(
        id=updated.id, name=updated.name, description=updated.description, icon=updated.icon,
        created_at=updated.created_at, updated_at=updated.updated_at, **counts,
    )


@router.delete("/{animal_type_id}", response_model=MessageResponse)
async def delete_animal_type(
    animal_type_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    item = await crud_animal_type.get_animal_type(db, animal_type_id)
    if not item:
        raise HTTPException(status_code=404, detail="Animal type not found.")
    await crud_animal_type.delete_animal_type(db, item)
    return MessageResponse(message=f"Animal type '{item.name}' deleted successfully.")
