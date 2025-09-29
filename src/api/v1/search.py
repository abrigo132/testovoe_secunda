from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings, db_helper
from core.schemas import GeoSearchResponse
from core.services import GeoSearchService
from core.exceptions import GeoSearchRadiusNotFoundOrganizations
from core.auth.dependecies import verify_auth_api_token

router = APIRouter(
    prefix=settings.api.v1.geo,
    tags=["Geographical Search"],
    dependencies=[Depends(verify_auth_api_token)],
)


@router.get("/search/radius/", response_model=GeoSearchResponse)
async def search_organizations_in_radius(
    lat: Annotated[float, Query(..., description="Широта центра")],
    lng: Annotated[float, Query(..., description="Долгота центра")],
    radius_km: Annotated[float, Query(..., description="Радиус в километрах")],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Поиск организаций в географическом радиусе

    Пример:
    /api/v1/geo/search/radius?lat=55.7558&lng=37.6173&radius_km=1.0

    Найдёт все организации в радиусе 1 км от координат [55.7558, 37.6173]
    """
    try:
        return await GeoSearchService(session=session).search_organizations_in_radius(
            lat, lng, radius_km
        )

    except GeoSearchRadiusNotFoundOrganizations as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
