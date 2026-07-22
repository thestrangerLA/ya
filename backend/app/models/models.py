"""
SQLAlchemy ORM Models for the Animal Medicine Information System.
Supports PostgreSQL and SQLite.
"""

import uuid
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    func,
    insert,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


# Helper for UUID type in SQLite/Postgres
def GUID_TYPE():
    return String(36)

def gen_uuid():
    return str(uuid.uuid4())


# ── Many-to-Many Junction ──────────────────────────────────────────────────
disease_medicines = Table(
    "disease_medicines",
    Base.metadata,
    Column(
        "disease_id",
        GUID_TYPE(),
        ForeignKey("diseases.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "medicine_id",
        GUID_TYPE(),
        ForeignKey("medicines.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# ── Animal Types ───────────────────────────────────────────────────────────
class AnimalType(Base):
    __tablename__ = "animal_types"

    id: Mapped[str] = mapped_column(
        GUID_TYPE(), primary_key=True, default=gen_uuid
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    medicines: Mapped[List["Medicine"]] = relationship(
        "Medicine", back_populates="animal_type", cascade="all, delete-orphan"
    )
    diseases: Mapped[List["Disease"]] = relationship(
        "Disease", back_populates="animal_type", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<AnimalType(id={self.id}, name='{self.name}')>"


# ── Categories ────────────────────────────────────────────────────────────
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        GUID_TYPE(), primary_key=True, default=gen_uuid
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    medicines: Mapped[List["Medicine"]] = relationship(
        "Medicine", back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"


# ── Medicines ─────────────────────────────────────────────────────────────
class Medicine(Base):
    __tablename__ = "medicines"

    id: Mapped[str] = mapped_column(
        GUID_TYPE(), primary_key=True, default=gen_uuid
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    brand: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sku: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)

    animal_type_id: Mapped[Optional[str]] = mapped_column(
        GUID_TYPE(), ForeignKey("animal_types.id", ondelete="SET NULL"), nullable=True
    )
    category_id: Mapped[Optional[str]] = mapped_column(
        GUID_TYPE(), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    indications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dosage: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    usage: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    warnings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    side_effects: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    storage: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    expiration_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    animal_type: Mapped[Optional["AnimalType"]] = relationship(
        "AnimalType", back_populates="medicines"
    )
    category: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="medicines"
    )
    images: Mapped[List["MedicineImage"]] = relationship(
        "MedicineImage",
        back_populates="medicine",
        cascade="all, delete-orphan",
        order_by="MedicineImage.sort_order",
    )
    recommended_for_diseases: Mapped[List["Disease"]] = relationship(
        "Disease",
        secondary=disease_medicines,
        back_populates="recommended_medicines",
    )

    def __repr__(self) -> str:
        return f"<Medicine(id={self.id}, name='{self.name}')>"


# ── Medicine Images ───────────────────────────────────────────────────────
class MedicineImage(Base):
    __tablename__ = "medicine_images"

    id: Mapped[str] = mapped_column(
        GUID_TYPE(), primary_key=True, default=gen_uuid
    )
    medicine_id: Mapped[str] = mapped_column(
        GUID_TYPE(), ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False
    )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    original_filename: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    medicine: Mapped["Medicine"] = relationship("Medicine", back_populates="images")

    def __repr__(self) -> str:
        return f"<MedicineImage(id={self.id}, medicine_id={self.medicine_id})>"


# ── Diseases ──────────────────────────────────────────────────────────────
class Disease(Base):
    __tablename__ = "diseases"

    id: Mapped[str] = mapped_column(
        GUID_TYPE(), primary_key=True, default=gen_uuid
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    animal_type_id: Mapped[Optional[str]] = mapped_column(
        GUID_TYPE(), ForeignKey("animal_types.id", ondelete="SET NULL"), nullable=True
    )

    symptoms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    prevention: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    treatment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    animal_type: Mapped[Optional["AnimalType"]] = relationship(
        "AnimalType", back_populates="diseases"
    )
    recommended_medicines: Mapped[List["Medicine"]] = relationship(
        "Medicine",
        secondary=disease_medicines,
        back_populates="recommended_for_diseases",
    )

    def __repr__(self) -> str:
        return f"<Disease(id={self.id}, name='{self.name}')>"
