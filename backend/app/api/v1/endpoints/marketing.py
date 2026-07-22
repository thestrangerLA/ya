"""
AI Marketing API Endpoints — 9 Core Marketing Features.
All content is strictly generated using local database records.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_medicine
from app.db.database import get_db
from app.schemas.schemas import (
    MarketingCopyRequest,
    MarketingCopyResponse,
    CampaignRequest,
    CampaignResponse,
    ImagePromptRequest,
    ImagePromptResponse,
    SocialContentRequest,
    SocialContentResponse,
    MarketingIdeasResponse,
    SEOContentResponse,
    ContentCalendarResponse,
    OneClickMarketingResponse,
)
from app.services.marketing_service import AIMarketingService

router = APIRouter(prefix="/marketing", tags=["AI Marketing"])


@router.post("/copy", response_model=MarketingCopyResponse)
async def generate_marketing_copy(
    req: MarketingCopyRequest,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, req.medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    res = AIMarketingService.generate_marketing_copy(medicine, tone=req.tone, target_audience=req.target_audience or "เกษตรกรและคนเลี้ยงสัตว์")
    return MarketingCopyResponse(**res)


@router.post("/campaign", response_model=CampaignResponse)
async def generate_campaign(
    req: CampaignRequest,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, req.medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    res = AIMarketingService.generate_campaign(medicine, campaign_type=req.campaign_type)
    return CampaignResponse(**res)


@router.post("/image-prompt", response_model=ImagePromptResponse)
async def generate_image_prompts(
    req: ImagePromptRequest,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, req.medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    res = AIMarketingService.generate_image_prompts(medicine, color_theme=req.color_theme, marketing_goal=req.marketing_goal)
    return ImagePromptResponse(**res)


@router.post("/social-content", response_model=SocialContentResponse)
async def generate_social_content(
    req: SocialContentRequest,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, req.medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    res = AIMarketingService.generate_social_content(medicine)
    return SocialContentResponse(**res)


@router.post("/ideas", response_model=MarketingIdeasResponse)
async def generate_ideas():
    res = AIMarketingService.generate_ideas()
    return MarketingIdeasResponse(**res)


@router.post("/seo", response_model=SEOContentResponse)
async def generate_seo(
    req: SocialContentRequest,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, req.medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    res = AIMarketingService.generate_seo(medicine)
    return SEOContentResponse(**res)


@router.post("/calendar", response_model=ContentCalendarResponse)
async def generate_calendar(
    req: SocialContentRequest,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, req.medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    res = AIMarketingService.generate_calendar(medicine)
    return ContentCalendarResponse(**res)


@router.post("/one-click", response_model=OneClickMarketingResponse)
async def generate_one_click(
    req: SocialContentRequest,
    db: AsyncSession = Depends(get_db),
):
    medicine = await crud_medicine.get_medicine(db, req.medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found.")
    res = AIMarketingService.generate_one_click(medicine)
    return OneClickMarketingResponse(**res)
