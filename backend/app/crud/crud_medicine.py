"""
CRUD utilities for Medicine and MedicineImage.
"""

import uuid
from datetime import date, timedelta
from typing import List, Optional, Tuple

from sqlalchemy import func, or_, select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.models import Medicine, MedicineImage, AnimalType, Category
from app.schemas.schemas import MedicineCreate, MedicineUpdate


# ── Medicine CRUD ──────────────────────────────────────────────────────────

async def get_medicine(db: AsyncSession, medicine_id: str) -> Optional[Medicine]:
    result = await db.execute(
        select(Medicine)
        .options(
            selectinload(Medicine.images),
            selectinload(Medicine.animal_type),
            selectinload(Medicine.category),
        )
        .where(Medicine.id == str(medicine_id))
    )
    return result.scalar_one_or_none()


async def get_medicines(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    animal_type_id: Optional[str] = None,
    category_id: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    low_stock_only: bool = False,
    expiring_only: bool = False,
) -> Tuple[List[Medicine], int]:
    query = select(Medicine).options(
        selectinload(Medicine.images),
        selectinload(Medicine.animal_type),
        selectinload(Medicine.category),
    )

    # ── Filters ──────────────────────────────────────────────────────────────
    conditions = []
    if animal_type_id:
        conditions.append(Medicine.animal_type_id == str(animal_type_id))
    if category_id:
        conditions.append(Medicine.category_id == str(category_id))
    if search:
        pattern = f"%{search}%"
        conditions.append(
            or_(
                Medicine.name.ilike(pattern),
                Medicine.brand.ilike(pattern),
                Medicine.sku.ilike(pattern),
                Medicine.description.ilike(pattern),
            )
        )
    if low_stock_only:
        conditions.append(Medicine.stock_quantity <= settings.LOW_STOCK_THRESHOLD)
    if expiring_only:
        cutoff = date.today() + timedelta(days=settings.EXPIRY_ALERT_DAYS)
        conditions.append(Medicine.expiration_date <= cutoff)
        conditions.append(Medicine.expiration_date >= date.today())

    if conditions:
        from sqlalchemy import and_
        query = query.where(and_(*conditions))

    # ── Count ─────────────────────────────────────────────────────────────────
    count_query = select(func.count()).select_from(
        query.with_only_columns(Medicine.id).subquery()
    )
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # ── Sort ──────────────────────────────────────────────────────────────────
    sort_column = getattr(Medicine, sort_by, Medicine.created_at)
    sort_fn = desc if sort_order == "desc" else asc
    query = query.order_by(sort_fn(sort_column)).offset(skip).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all()), total


async def create_medicine(db: AsyncSession, data: MedicineCreate) -> Medicine:
    db_obj = Medicine(**data.model_dump())
    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj, ["animal_type", "category"])
    return db_obj


async def update_medicine(
    db: AsyncSession,
    db_obj: Medicine,
    data: MedicineUpdate,
) -> Medicine:
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    await db.flush()
    await db.refresh(db_obj, ["animal_type", "category", "images"])
    return db_obj


async def delete_medicine(db: AsyncSession, db_obj: Medicine) -> None:
    from app.models.models import disease_medicines
    from app.services.file_storage import file_storage_service
    # Delete junction table entries
    await db.execute(disease_medicines.delete().where(disease_medicines.c.medicine_id == db_obj.id))
    # Remove files from local storage
    for img in db_obj.images:
        await file_storage_service.delete_file(img.file_path)
    await db.delete(db_obj)
    await db.flush()


# ── MedicineImage CRUD ─────────────────────────────────────────────────────

async def get_medicine_image(
    db: AsyncSession, image_id: uuid.UUID
) -> Optional[MedicineImage]:
    result = await db.execute(
        select(MedicineImage).where(MedicineImage.id == image_id)
    )
    return result.scalar_one_or_none()


async def create_medicine_image(
    db: AsyncSession,
    medicine_id: uuid.UUID,
    file_path: str,
    original_filename: str,
    file_size: int,
    mime_type: str,
    is_primary: bool = False,
) -> MedicineImage:
    # If marked primary, demote existing primaries
    if is_primary:
        await db.execute(
            MedicineImage.__table__.update()
            .where(MedicineImage.medicine_id == medicine_id)
            .values(is_primary=False)
        )

    # Compute sort order
    count_result = await db.execute(
        select(func.count()).select_from(MedicineImage).where(
            MedicineImage.medicine_id == medicine_id
        )
    )
    sort_order = count_result.scalar_one()

    db_image = MedicineImage(
        medicine_id=medicine_id,
        file_path=file_path,
        original_filename=original_filename,
        file_size=file_size,
        mime_type=mime_type,
        is_primary=is_primary,
        sort_order=sort_order,
    )
    db.add(db_image)
    await db.flush()
    await db.refresh(db_image)
    return db_image


async def set_primary_image(
    db: AsyncSession, medicine_id: uuid.UUID, image_id: uuid.UUID
) -> None:
    await db.execute(
        MedicineImage.__table__.update()
        .where(MedicineImage.medicine_id == medicine_id)
        .values(is_primary=False)
    )
    await db.execute(
        MedicineImage.__table__.update()
        .where(MedicineImage.id == image_id)
        .values(is_primary=True)
    )
    await db.flush()


async def delete_medicine_image(db: AsyncSession, db_obj: MedicineImage) -> None:
    await db.delete(db_obj)
    await db.flush()


# ── Dashboard / Stats ──────────────────────────────────────────────────────

async def get_medicine_stats(db: AsyncSession) -> dict:
    total = (await db.execute(select(func.count()).select_from(Medicine))).scalar_one()

    low_stock = (
        await db.execute(
            select(func.count())
            .select_from(Medicine)
            .where(Medicine.stock_quantity <= settings.LOW_STOCK_THRESHOLD)
        )
    ).scalar_one()

    cutoff = date.today() + timedelta(days=settings.EXPIRY_ALERT_DAYS)
    expiring = (
        await db.execute(
            select(func.count())
            .select_from(Medicine)
            .where(Medicine.expiration_date <= cutoff)
            .where(Medicine.expiration_date >= date.today())
        )
    ).scalar_one()

    return {
        "total": total,
        "low_stock": low_stock,
        "expiring_soon": expiring,
    }


async def get_recent_medicines(db: AsyncSession, limit: int = 5) -> List[Medicine]:
    result = await db.execute(
        select(Medicine)
        .options(selectinload(Medicine.images), selectinload(Medicine.animal_type))
        .order_by(desc(Medicine.created_at))
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_low_stock_medicines(
    db: AsyncSession, limit: int = 50
) -> List[Medicine]:
    result = await db.execute(
        select(Medicine)
        .options(selectinload(Medicine.images), selectinload(Medicine.animal_type))
        .where(Medicine.stock_quantity <= settings.LOW_STOCK_THRESHOLD)
        .order_by(asc(Medicine.stock_quantity))
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_expiring_medicines(db: AsyncSession, limit: int = 50) -> List[Medicine]:
    cutoff = date.today() + timedelta(days=settings.EXPIRY_ALERT_DAYS)
    result = await db.execute(
        select(Medicine)
        .options(selectinload(Medicine.images), selectinload(Medicine.animal_type))
        .where(Medicine.expiration_date <= cutoff)
        .where(Medicine.expiration_date >= date.today())
        .order_by(asc(Medicine.expiration_date))
        .limit(limit)
    )
    return list(result.scalars().all())
