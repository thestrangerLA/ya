"""
API v1 router — aggregates all endpoint routers.
"""

from fastapi import APIRouter

from app.api.v1.endpoints.animal_types import router as animal_types_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.medicines import router as medicines_router
from app.api.v1.endpoints.diseases import router as diseases_router
from app.api.v1.endpoints.marketing import router as marketing_router
from app.api.v1.endpoints.misc import (
    dashboard_router,
    search_router,
    ai_router,
    inventory_router,
)

api_router = APIRouter()

api_router.include_router(animal_types_router)
api_router.include_router(categories_router)
api_router.include_router(medicines_router)
api_router.include_router(diseases_router)
api_router.include_router(marketing_router)
api_router.include_router(dashboard_router)
api_router.include_router(search_router)
api_router.include_router(ai_router)
api_router.include_router(inventory_router)
