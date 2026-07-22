"""
Disease API endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_disease
from app.db.database import get_db
from app.schemas.schemas import (
    DiseaseCreate,
    DiseaseListRead,
    DiseaseRead,
    DiseaseUpdate,
    MessageResponse,
    PaginatedResponse,
    PaginationMeta,
)

router = APIRouter(prefix="/diseases", tags=["Diseases"])


@router.get("/", response_model=PaginatedResponse[DiseaseListRead])
async def list_diseases(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    animal_type_id: Optional[str] = Query(default=None),
    sort_by: str = Query(default="created_at", pattern="^(name|created_at)$"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
):
    skip = (page - 1) * page_size
    items, total = await crud_disease.get_diseases(
        db, skip=skip, limit=page_size,
        animal_type_id=animal_type_id, search=search,
        sort_by=sort_by, sort_order=sort_order,
    )
    result = [
        DiseaseListRead(
            id=str(d.id), name=d.name, symptoms=d.symptoms, created_at=d.created_at,
            animal_type=d.animal_type,
            medicine_count=len(d.recommended_medicines),
        )
        for d in items
    ]
    total_pages = max(1, -(-total // page_size))
    return PaginatedResponse(
        data=result,
        meta=PaginationMeta(total=total, page=page, page_size=page_size, total_pages=total_pages),
    )


@router.post("/", response_model=DiseaseRead, status_code=status.HTTP_201_CREATED)
async def create_disease(
    data: DiseaseCreate,
    db: AsyncSession = Depends(get_db),
):
    disease = await crud_disease.create_disease(db, data)
    return DiseaseRead.model_validate(disease)


@router.get("/{disease_id}", response_model=DiseaseRead)
async def get_disease(
    disease_id: str,
    db: AsyncSession = Depends(get_db),
):
    disease = await crud_disease.get_disease(db, str(disease_id))
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found.")
    return DiseaseRead.model_validate(disease)


@router.patch("/{disease_id}", response_model=DiseaseRead)
async def update_disease(
    disease_id: str,
    data: DiseaseUpdate,
    db: AsyncSession = Depends(get_db),
):
    disease = await crud_disease.get_disease(db, str(disease_id))
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found.")
    updated = await crud_disease.update_disease(db, disease, data)
    return DiseaseRead.model_validate(updated)


@router.delete("/{disease_id}", response_model=MessageResponse)
async def delete_disease(
    disease_id: str,
    db: AsyncSession = Depends(get_db),
):
    disease = await crud_disease.get_disease(db, str(disease_id))
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found.")
    await crud_disease.delete_disease(db, disease)
    return MessageResponse(message=f"Disease '{disease.name}' deleted successfully.")
