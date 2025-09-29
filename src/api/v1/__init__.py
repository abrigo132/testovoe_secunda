from fastapi import APIRouter

from core import settings
from .organization import router as organization_router
from .building import router as building_router
from .activity import router as activity_router
from .search import router as search_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(organization_router)
router.include_router(building_router)

router.include_router(activity_router)

router.include_router(search_router)
