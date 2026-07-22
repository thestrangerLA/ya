"""
CRUD utilities for Disease.
"""

import uuid
from typing import List, Optional, Tuple

from sqlalchemy import func, or_, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import Disease, Medicine, disease_medicines
from app.schemas.schemas import DiseaseCreate, DiseaseUpdate


async def get_disease(db: AsyncSession, disease_id: str) -> Optional[Disease]:
    result = await db.execute(
        select(Disease)
        .options(
            selectinload(Disease.animal_type),
            selectinload(Disease.recommended_medicines).selectinload(Medicine.images),
            selectinload(Disease.recommended_medicines).selectinload(Medicine.animal_type),
        )
        .where(Disease.id == str(disease_id))
    )
    return result.scalar_one_or_none()


async def get_diseases(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    animal_type_id: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> Tuple[List[Disease], int]:
    query = select(Disease).options(
        selectinload(Disease.animal_type),
        selectinload(Disease.recommended_medicines),
    )

    conditions = []
    if animal_type_id:
        conditions.append(Disease.animal_type_id == str(animal_type_id))
    if search:
        pattern = f"%{search}%"
        conditions.append(
            or_(
                Disease.name.ilike(pattern),
                Disease.symptoms.ilike(pattern),
                Disease.cause.ilike(pattern),
                Disease.treatment.ilike(pattern),
            )
        )

    if conditions:
        from sqlalchemy import and_
        query = query.where(and_(*conditions))

    # Count
    count_query = select(func.count()).select_from(
        query.with_only_columns(Disease.id).subquery()
    )
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # Sort
    sort_column = getattr(Disease, sort_by, Disease.created_at)
    from sqlalchemy import desc as desc_fn, asc as asc_fn
    sort_fn = desc_fn if sort_order == "desc" else asc_fn
    query = query.order_by(sort_fn(sort_column)).offset(skip).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all()), total


async def create_disease(db: AsyncSession, data: DiseaseCreate) -> Disease:
    medicine_ids = data.recommended_medicine_ids
    disease_data = data.model_dump(exclude={"recommended_medicine_ids"})

    db_obj = Disease(**disease_data)

    if medicine_ids:
        medicines_result = await db.execute(
            select(Medicine).where(Medicine.id.in_(medicine_ids))
        )
        db_obj.recommended_medicines = list(medicines_result.scalars().all())

    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj, ["animal_type", "recommended_medicines"])
    return db_obj


async def update_disease(
    db: AsyncSession,
    db_obj: Disease,
    data: DiseaseUpdate,
) -> Disease:
    update_data = data.model_dump(exclude_unset=True, exclude={"recommended_medicine_ids"})
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    if data.recommended_medicine_ids is not None:
        if data.recommended_medicine_ids:
            medicines_result = await db.execute(
                select(Medicine).where(Medicine.id.in_(data.recommended_medicine_ids))
            )
            db_obj.recommended_medicines = list(medicines_result.scalars().all())
        else:
            db_obj.recommended_medicines = []

    await db.flush()
    await db.refresh(db_obj, ["animal_type", "recommended_medicines"])
    return db_obj


async def delete_disease(db: AsyncSession, db_obj: Disease) -> None:
    from app.models.models import disease_medicines
    await db.execute(disease_medicines.delete().where(disease_medicines.c.disease_id == db_obj.id))
    await db.delete(db_obj)
    await db.flush()


async def get_disease_count(db: AsyncSession) -> int:
    result = await db.execute(select(func.count()).select_from(Disease))
    return result.scalar_one()
