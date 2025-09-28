from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core import settings, db_helper
from core.schemas import OrganizationDetailResponse
from core.services import OrganizationService
from core.exceptions import OrganizationNotFoundById, OrganizationNotFoundByName
from core.auth.dependecies import verify_auth_api_token

router = APIRouter(
    prefix=settings.api.v1.organization,
    tags=["Organization"],
    dependencies=[Depends(verify_auth_api_token)],
)


@router.get("/{organization_id}/", response_model=OrganizationDetailResponse)
async def get_organization(
    organization_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        organization = await OrganizationService(session=session).get_by_id(
            organization_id=organization_id,
        )
        return OrganizationDetailResponse.model_validate(organization)
    except OrganizationNotFoundById as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{organization_name}/", response_model=OrganizationDetailResponse)
async def get_organization(
    organization_name: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        organization = await OrganizationService(session=session).get_by_name(
            organization_name=organization_name,
        )
        return OrganizationDetailResponse.model_validate(organization)
    except OrganizationNotFoundByName as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
