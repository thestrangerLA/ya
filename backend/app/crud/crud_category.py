"""
CRUD utilities for Category.
"""

import uuid
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Category, Medicine
from app.schemas.schemas import CategoryCreate, CategoryUpdate


async def get_category(db: AsyncSession, category_id: str) -> Optional[Category]:
    result = await db.execute(select(Category).where(Category.id == str(category_id)))
    return result.scalar_one_or_none()


async def get_category_by_name(db: AsyncSession, name: str) -> Optional[Category]:
    result = await db.execute(select(Category).where(Category.name == name))
    return result.scalar_one_or_none()


async def get_categories(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> tuple[List[Category], int]:
    count_result = await db.execute(select(func.count()).select_from(Category))
    total = count_result.scalar_one()

    result = await db.execute(
        select(Category).order_by(Category.name).offset(skip).limit(limit)
    )
    items = result.scalars().all()
    return list(items), total


async def create_category(db: AsyncSession, data: CategoryCreate) -> Category:
    db_obj = Category(**data.model_dump())
    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def update_category(
    db: AsyncSession,
    db_obj: Category,
    data: CategoryUpdate,
) -> Category:
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def delete_category(db: AsyncSession, db_obj: Category) -> None:
    await db.delete(db_obj)
    await db.flush()


async def get_category_medicine_count(db: AsyncSession, category_id: uuid.UUID) -> int:
    result = await db.execute(
        select(func.count()).select_from(Medicine).where(Medicine.category_id == category_id)
    )
    return result.scalar_one()
