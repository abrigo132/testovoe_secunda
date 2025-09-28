from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession

from core import settings, db_helper
from core.exceptions import ActivityNotFound, ActivityNotFoundPathTree
from core.schemas import ActivityWithOrganizationResponse
from core.schemas.base import OrganizationShort
from core.services import ActivityService
from core.auth.dependecies import verify_auth_api_token


router = APIRouter(
    prefix=settings.api.v1.activity,
    tags=["Activity"],
    dependencies=[Depends(verify_auth_api_token)],
)


@router.get(
    "/{activity_name}/organizations/", response_model=ActivityWithOrganizationResponse
)
async def get_activity_with_organization(
    activity_name: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        activity = await ActivityService(
            session=session
        ).get_activity_by_name_with_organizations(
            activity_name=activity_name,
        )
        return ActivityWithOrganizationResponse.model_validate(activity)

    except ActivityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/search/organizations/", response_model=List[OrganizationShort])
async def search_organizations_by_activity_tree(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    activity_path: str = Query(..., description="LTREE path, например: 'еда'"),
):
    """
    Простой поиск: все организации в дереве деятельности
    Пример: /api/v1/activities/search/organizations?activity_path=еда
    Найдёт организации для: Еда, Мясная продукция, Молочная продукция
    """
    try:
        organizations = await ActivityService(
            session=session
        ).search_organizations_by_activity_tree(activity_path)
        return [OrganizationShort.model_validate(org) for org in organizations]
    except ActivityNotFoundPathTree as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
