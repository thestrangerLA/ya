"""
Medicine API endpoints — full CRUD + image upload/delete.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_medicine
from app.db.database import get_db
from app.schemas.schemas import (
    MedicineCreate,
    MedicineListRead,
    MedicineRead,
    MedicineUpdate,
    MedicineImageRead,
    MessageResponse,
    PaginatedResponse,
    PaginationMeta,
)
from app.services.file_storage import file_storage_service

router = APIRouter(prefix="/medicines", tags=["Medicines"])


def _build_image_url(request: Request, file_path: str) -> str:
    base = str(request.base_url).rstrip("/")
    return f"{base}/api/v1/files/{file_path}"


def _enrich_medicine_read(medicine, request: Request) -> MedicineRead:
    """Attach full URLs to MedicineImage records."""
    images = []
    for img in (medicine.images or []):
        images.append(
            MedicineImageRead(
                id=str(img.id),
                medicine_id=str(img.medicine_id),
                file_path=img.file_path,
                original_filename=img.original_filename,
                file_size=img.file_size,
                mime_type=img.mime_type,
                is_primary=img.is_primary,
                sort_order=img.sort_order,
                created_at=img.created_at,
                url=_build_image_url(request, img.file_path),
            )
        )
    return MedicineRead(
        id=str(medicine.id),
        name=medicine.name,
        brand=medicine.brand,
        sku=medicine.sku,
        animal_type_id=str(medicine.animal_type_id) if medicine.animal_type_id else None,
        category_id=str(medicine.category_id) if medicine.category_id else None,
        description=medicine.description,
        indications=medicine.indications,
        dosage=medicine.dosage,
        usage=medicine.usage,
        warnings=medicine.warnings,
        side_effects=medicine.side_effects,
        storage=medicine.storage,
        notes=medicine.notes,
        expiration_date=medicine.expiration_date,
        stock_quantity=medicine.stock_quantity,
        price=medicine.price,
        created_at=medicine.created_at,
        updated_at=medicine.updated_at,
        animal_type=medicine.animal_type,
        category=medicine.category,
        images=images,
    )


# ── List ───────────────────────────────────────────────────────────────────

@router.get("/", response_model=PaginatedResponse[MedicineListRead])
async def list_medicines(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    animal_type_id: Optional[str] = Query(default=None),
    category_id: Optional[str] = Query(default=None),
    sort_by: str = Query(default="created_at", pattern="^(name|brand|stock_quantity|price|expiration_date|created_at)$"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    low_stock_only: bool = Query(default=False),
    expiring_only: bool = Query(default=False),
    db: AsyncSession = Depends(get_db),
):
    skip = (page - 1) * page_size
    items, total = await crud_medicine.get_medicines(
        db, skip=skip, limit=page_size,
        animal_type_id=animal_type_id, category_id=category_id,
        search=search, sort_by=sort_by, sort_order=sort_order,
        low_stock_only=low_stock_only, expiring_only=expiring_only,
    )
    result = []
    for med in items:
        primary_url = None
        if med.images:
            primary = next((img for img in med.images if img.is_primary), med.images[0] if med.images else None)
            if primary:
                primary_url = _build_image_url(request, primary.file_path)
        result.append(
            MedicineListRead(
                id=str(med.id), name=med.name, brand=med.brand, sku=med.sku,
                stock_quantity=med.stock_quantity, price=med.price,
                expiration_date=med.expiration_date, created_at=med.created_at,
                animal_type=med.animal_type, category=med.category,
                primary_image_url=primary_url,
            )
        )
    total_pages = max(1, -(-total // page_size))
    return PaginatedResponse(
        data=result,
        meta=PaginationMeta(total=total, page=page, page_size=page_size, total_pages=total_pages),
    )


# ── Create ─────────────────────────────────────────────────────────────────

@router.post("/", response_model=MedicineRead, status_code=status.HTTP_201_CREATED)
async def create_medicine(
    request: Request,
    data: MedicineCreate,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.create_medicine(db, data)
    return _enrich_medicine_read(medicine, request)


# ── Get One ────────────────────────────────────────────────────────────────

@router.get("/{medicine_id}", response_model=MedicineRead)
async def get_medicine(
    medicine_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, str(medicine_id))
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    return _enrich_medicine_read(medicine, request)


# ── Update ─────────────────────────────────────────────────────────────────

@router.patch("/{medicine_id}", response_model=MedicineRead)
async def update_medicine(
    medicine_id: str,
    request: Request,
    data: MedicineUpdate,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, str(medicine_id))
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    updated = await crud_medicine.update_medicine(db, medicine, data)
    return _enrich_medicine_read(updated, request)


# ── Delete ─────────────────────────────────────────────────────────────────

@router.delete("/{medicine_id}", response_model=MessageResponse)
async def delete_medicine(
    medicine_id: str,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, str(medicine_id))
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    await crud_medicine.delete_medicine(db, medicine)
    return MessageResponse(message=f"Medicine '{medicine.name}' deleted successfully.")


# ── Image Upload ───────────────────────────────────────────────────────────

@router.post("/{medicine_id}/images", response_model=MedicineImageRead, status_code=status.HTTP_201_CREATED)
async def upload_medicine_image(
    medicine_id: str,
    request: Request,
    file: UploadFile = File(...),
    is_primary: bool = Query(default=False),
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, str(medicine_id))
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")

    if not medicine.images:
        is_primary = True

    saved = await file_storage_service.save_image(file, str(medicine_id))
    image = await crud_medicine.create_medicine_image(
        db,
        medicine_id=str(medicine_id),
        file_path=saved["file_path"],
        original_filename=saved["original_filename"],
        file_size=saved["file_size"],
        mime_type=saved["mime_type"],
        is_primary=is_primary,
    )
    return MedicineImageRead(
        id=str(image.id), medicine_id=str(image.medicine_id), file_path=image.file_path,
        original_filename=image.original_filename, file_size=image.file_size,
        mime_type=image.mime_type, is_primary=image.is_primary, sort_order=image.sort_order,
        created_at=image.created_at,
        url=_build_image_url(request, image.file_path),
    )


@router.post("/{medicine_id}/images/batch", response_model=List[MedicineImageRead], status_code=status.HTTP_201_CREATED)
async def upload_multiple_images(
    medicine_id: str,
    request: Request,
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, str(medicine_id))
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")

    results = []
    for i, file in enumerate(files):
        is_primary = (i == 0 and not medicine.images)
        saved = await file_storage_service.save_image(file, str(medicine_id))
        image = await crud_medicine.create_medicine_image(
            db,
            medicine_id=str(medicine_id),
            file_path=saved["file_path"],
            original_filename=saved["original_filename"],
            file_size=saved["file_size"],
            mime_type=saved["mime_type"],
            is_primary=is_primary,
        )
        results.append(
            MedicineImageRead(
                id=str(image.id), medicine_id=str(image.medicine_id), file_path=image.file_path,
                original_filename=image.original_filename, file_size=image.file_size,
                mime_type=image.mime_type, is_primary=image.is_primary, sort_order=image.sort_order,
                created_at=image.created_at,
                url=_build_image_url(request, image.file_path),
            )
        )
    return results


@router.patch("/{medicine_id}/images/{image_id}/set-primary", response_model=MessageResponse)
async def set_primary_image(
    medicine_id: str,
    image_id: str,
    db: AsyncSession = Depends(get_db),
):
    image = await crud_medicine.get_medicine_image(db, str(image_id))
    if not image or str(image.medicine_id) != str(medicine_id):
        raise HTTPException(status_code=404, detail="Image not found.")
    await crud_medicine.set_primary_image(db, str(medicine_id), str(image_id))
    return MessageResponse(message="Primary image updated.")


@router.delete("/{medicine_id}/images/{image_id}", response_model=MessageResponse)
async def delete_medicine_image(
    medicine_id: str,
    image_id: str,
    db: AsyncSession = Depends(get_db),
):
    image = await crud_medicine.get_medicine_image(db, str(image_id))
    if not image or str(image.medicine_id) != str(medicine_id):
        raise HTTPException(status_code=404, detail="Image not found.")
    await file_storage_service.delete_file(image.file_path)
    await crud_medicine.delete_medicine_image(db, image)
    return MessageResponse(message="Image deleted successfully.")
