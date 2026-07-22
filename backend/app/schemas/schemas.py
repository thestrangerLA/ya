"""
Pydantic schemas for request/response validation.

Schemas are organized by domain:
    - AnimalType
    - Category
    - Medicine + MedicineImage
    - Disease
    - Pagination / Common
    - AI Assistant
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ══════════════════════════════════════════════════════════════════════════════
# Common / Pagination
# ══════════════════════════════════════════════════════════════════════════════

DataT = TypeVar("DataT")


class PaginationMeta(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[DataT]):
    data: List[DataT]
    meta: PaginationMeta


class MessageResponse(BaseModel):
    message: str
    success: bool = True


# ══════════════════════════════════════════════════════════════════════════════
# AnimalType Schemas
# ══════════════════════════════════════════════════════════════════════════════

class AnimalTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None


class AnimalTypeCreate(AnimalTypeBase):
    pass


class AnimalTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None


class AnimalTypeRead(AnimalTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    medicine_count: Optional[int] = 0
    disease_count: Optional[int] = 0


# ══════════════════════════════════════════════════════════════════════════════
# Category Schemas
# ══════════════════════════════════════════════════════════════════════════════

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    medicine_count: Optional[int] = 0


# ══════════════════════════════════════════════════════════════════════════════
# MedicineImage Schemas
# ══════════════════════════════════════════════════════════════════════════════

class MedicineImageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    medicine_id: uuid.UUID
    file_path: str
    original_filename: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    is_primary: bool
    sort_order: int
    created_at: datetime
    url: Optional[str] = None  # computed field for API URL


# ══════════════════════════════════════════════════════════════════════════════
# Medicine Schemas
# ══════════════════════════════════════════════════════════════════════════════

class MedicineBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    brand: Optional[str] = Field(None, max_length=255)
    sku: Optional[str] = Field(None, max_length=100)
    animal_type_id: Optional[uuid.UUID] = None
    category_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    indications: Optional[str] = None
    dosage: Optional[str] = None
    usage: Optional[str] = None
    warnings: Optional[str] = None
    side_effects: Optional[str] = None
    storage: Optional[str] = None
    notes: Optional[str] = None
    expiration_date: Optional[date] = None
    stock_quantity: int = Field(default=0, ge=0)
    price: Optional[Decimal] = Field(None, ge=0)


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    brand: Optional[str] = Field(None, max_length=255)
    sku: Optional[str] = Field(None, max_length=100)
    animal_type_id: Optional[uuid.UUID] = None
    category_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    indications: Optional[str] = None
    dosage: Optional[str] = None
    usage: Optional[str] = None
    warnings: Optional[str] = None
    side_effects: Optional[str] = None
    storage: Optional[str] = None
    notes: Optional[str] = None
    expiration_date: Optional[date] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    price: Optional[Decimal] = Field(None, ge=0)


class MedicineListRead(BaseModel):
    """Lightweight schema for list views."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    brand: Optional[str] = None
    sku: Optional[str] = None
    stock_quantity: int
    price: Optional[Decimal] = None
    expiration_date: Optional[date] = None
    created_at: datetime
    animal_type: Optional[AnimalTypeRead] = None
    category: Optional[CategoryRead] = None
    primary_image_url: Optional[str] = None


class MedicineRead(MedicineBase):
    """Full schema for detail views."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    animal_type: Optional[AnimalTypeRead] = None
    category: Optional[CategoryRead] = None
    images: List[MedicineImageRead] = []


# ══════════════════════════════════════════════════════════════════════════════
# Disease Schemas
# ══════════════════════════════════════════════════════════════════════════════

class DiseaseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    animal_type_id: Optional[uuid.UUID] = None
    symptoms: Optional[str] = None
    cause: Optional[str] = None
    prevention: Optional[str] = None
    treatment: Optional[str] = None


class DiseaseCreate(DiseaseBase):
    recommended_medicine_ids: List[uuid.UUID] = []


class DiseaseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    animal_type_id: Optional[uuid.UUID] = None
    symptoms: Optional[str] = None
    cause: Optional[str] = None
    prevention: Optional[str] = None
    treatment: Optional[str] = None
    recommended_medicine_ids: Optional[List[uuid.UUID]] = None


class DiseaseListRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    symptoms: Optional[str] = None
    created_at: datetime
    animal_type: Optional[AnimalTypeRead] = None
    medicine_count: Optional[int] = 0


class DiseaseRead(DiseaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    animal_type: Optional[AnimalTypeRead] = None
    recommended_medicines: List[MedicineListRead] = []


# ══════════════════════════════════════════════════════════════════════════════
# Dashboard Schemas
# ══════════════════════════════════════════════════════════════════════════════

class DashboardStats(BaseModel):
    total_medicines: int
    total_diseases: int
    total_animal_types: int
    low_stock_count: int
    expiring_soon_count: int


class RecentMedicine(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    brand: Optional[str] = None
    stock_quantity: int
    created_at: datetime
    primary_image_url: Optional[str] = None
    animal_type_name: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════════════
# Search Schemas
# ══════════════════════════════════════════════════════════════════════════════

class SearchFilters(BaseModel):
    query: str = Field(..., min_length=1)
    animal_type_id: Optional[uuid.UUID] = None
    category_id: Optional[uuid.UUID] = None
    search_type: Optional[str] = Field(None, pattern="^(medicine|disease|all)$")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class SearchResult(BaseModel):
    medicines: List[MedicineListRead] = []
    diseases: List[DiseaseListRead] = []
    total_medicines: int = 0
    total_diseases: int = 0
    query: str


# ══════════════════════════════════════════════════════════════════════════════
# AI Assistant Schemas
# ══════════════════════════════════════════════════════════════════════════════

class AIQuery(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    animal_type_id: Optional[uuid.UUID] = None


class AIRecommendedMedicine(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    brand: Optional[str] = None
    dosage: Optional[str] = None
    warnings: Optional[str] = None
    stock_quantity: int
    primary_image_url: Optional[str] = None


class AIMatchedDisease(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    symptoms: Optional[str] = None
    treatment: Optional[str] = None
    animal_type_name: Optional[str] = None
    recommended_medicines: List[AIRecommendedMedicine] = []
    match_score: float = 0.0
    matched_keywords: List[str] = []


class AIResponse(BaseModel):
    query: str
    interpretation: str
    possible_diseases: List[AIMatchedDisease] = []
    all_recommended_medicines: List[AIRecommendedMedicine] = []
    disclaimer: str = (
        "This information is based solely on records in the local database. "
        "Always consult a licensed veterinarian for medical advice."
    )


# ══════════════════════════════════════════════════════════════════════════════
# Inventory Schemas
# ══════════════════════════════════════════════════════════════════════════════

class LowStockItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    brand: Optional[str] = None
    stock_quantity: int
    primary_image_url: Optional[str] = None
    animal_type_name: Optional[str] = None


class ExpiringItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    brand: Optional[str] = None
    expiration_date: date
    stock_quantity: int
    days_until_expiry: int
    primary_image_url: Optional[str] = None


class InventoryReport(BaseModel):
    low_stock_items: List[LowStockItem] = []
    expiring_items: List[ExpiringItem] = []
    total_low_stock: int = 0
    total_expiring: int = 0
    total_stock_value: Optional[Decimal] = None


# ══════════════════════════════════════════════════════════════════════════════
# AI Marketing Schemas
# ══════════════════════════════════════════════════════════════════════════════

class MarketingCopyRequest(BaseModel):
    medicine_id: str
    tone: str = "Professional"  # Professional, Friendly, Funny, Emotional, Urgency, Luxury, Educational, Storytelling
    target_audience: Optional[str] = "เกษตรกรและคนเลี้ยงสัตว์"


class MarketingCopyResponse(BaseModel):
    facebook_post: str
    short_caption: str
    long_caption: str
    promotional_text: str
    product_description: str
    call_to_action: str
    headline: str
    hook: str
    customer_benefit: str
    bullet_points: List[str]
    faq: List[dict]


class CampaignRequest(BaseModel):
    medicine_id: str
    campaign_type: str = "Flash Sale"  # Flash Sale, New Product, Holiday Promotion, Bundle Promotion, Seasonal Promotion, Free Shipping, Discount, Limited Time, Buy One Get One


class CampaignResponse(BaseModel):
    campaign_title: str
    campaign_type: str
    target_audience: str
    key_selling_point: str
    promotional_headline: str
    post_caption: str
    discount_structure: str
    call_to_action: str
    terms_and_conditions: str


class ImagePromptRequest(BaseModel):
    medicine_id: str
    color_theme: str = "Green & Gold"
    marketing_goal: str = "Premium Advertising Poster"


class ImagePromptResponse(BaseModel):
    medicine_name: str
    animal_type: str
    color_theme: str
    square_prompt: str
    portrait_prompt: str
    landscape_prompt: str


class SocialContentRequest(BaseModel):
    medicine_id: str


class SocialContentResponse(BaseModel):
    facebook: str
    instagram: str
    tiktok: str
    line_oa: str
    website: str
    hashtags: List[str]


class MarketingIdeasResponse(BaseModel):
    facebook_post_ideas: List[str]
    video_ideas: List[str]
    photo_ideas: List[str]
    promotion_ideas: List[str]
    educational_content_ideas: List[str]


class SEOContentResponse(BaseModel):
    product_description: str
    meta_description: str
    keywords: List[str]
    blog_article: str
    faq_schema: List[dict]


class ContentCalendarResponse(BaseModel):
    calendar_30_days: List[dict]  # day, facebook_post, promotion, educational_tip, engagement_idea


class OneClickMarketingResponse(BaseModel):
    medicine_name: str
    facebook_post: str
    short_caption: str
    long_caption: str
    headline: str
    promotion_text: str
    poster_prompt: str
    instagram_caption: str
    tiktok_caption: str
    line_oa_broadcast: str
    hashtags: List[str]
    seo_description: str
    marketing_ideas: List[str]

