from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core import settings, db_helper
from core.exceptions import BuildingNotFound
from core.schemas import BuildingWithOrganizationResponse
from core.services import BuildingService
from core.auth.dependecies import verify_auth_api_token

router = APIRouter(
    prefix=settings.api.v1.building,
    tags=["Building"],
    dependencies=[Depends(verify_auth_api_token)],
)


@router.get(
    "/{building_id}/organizations/",
    response_model=BuildingWithOrganizationResponse,
)
async def get_organization_from_building_address(
    building_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        building = await BuildingService(session=session).get_building_by_id(
            building_id=building_id,
        )
        return BuildingWithOrganizationResponse.model_validate(
            building, from_attributes=True
        )
    except BuildingNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
