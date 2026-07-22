"""
CRUD utilities for AnimalType.
"""

import uuid
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import AnimalType, Medicine, Disease
from app.schemas.schemas import AnimalTypeCreate, AnimalTypeUpdate


async def get_animal_type(db: AsyncSession, animal_type_id: str) -> Optional[AnimalType]:
    result = await db.execute(select(AnimalType).where(AnimalType.id == str(animal_type_id)))
    return result.scalar_one_or_none()


async def get_animal_type_by_name(db: AsyncSession, name: str) -> Optional[AnimalType]:
    result = await db.execute(select(AnimalType).where(AnimalType.name == name))
    return result.scalar_one_or_none()


async def get_animal_types(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> tuple[List[AnimalType], int]:
    count_result = await db.execute(select(func.count()).select_from(AnimalType))
    total = count_result.scalar_one()

    result = await db.execute(
        select(AnimalType).order_by(AnimalType.name).offset(skip).limit(limit)
    )
    items = result.scalars().all()
    return list(items), total


async def create_animal_type(db: AsyncSession, data: AnimalTypeCreate) -> AnimalType:
    db_obj = AnimalType(**data.model_dump())
    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def update_animal_type(
    db: AsyncSession,
    db_obj: AnimalType,
    data: AnimalTypeUpdate,
) -> AnimalType:
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def delete_animal_type(db: AsyncSession, db_obj: AnimalType) -> None:
    await db.delete(db_obj)
    await db.flush()


async def get_animal_type_counts(db: AsyncSession, animal_type_id: uuid.UUID) -> dict:
    med_count = await db.execute(
        select(func.count()).select_from(Medicine).where(Medicine.animal_type_id == animal_type_id)
    )
    dis_count = await db.execute(
        select(func.count()).select_from(Disease).where(Disease.animal_type_id == animal_type_id)
    )
    return {
        "medicine_count": med_count.scalar_one(),
        "disease_count": dis_count.scalar_one(),
    }
