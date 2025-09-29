from fastapi import APIRouter, Depends, status, Path
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


@router.get(
    "/{organization_id}/detail_id/",
    response_model=OrganizationDetailResponse,
    summary="Получить организацию по ID",
    description="Возвращает полную информацию об организации по её уникальному идентификатору",
    response_description="Детальная информация об организации включая контакты, адрес и виды деятельности",
)
async def get_organization_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    organization_id: int = Path(
        ..., description="Уникальный идентификатор организации", example=1
    ),
):
    """
    Получение детальной информации об организации по ID.

    - **organization_id**: Уникальный числовой идентификатор организации в системе
    - **Возвращает**: Полную информацию об организации включая:
        - Основные данные (название, ID)
        - Контактные телефоны
        - Адрес здания с координатами
        - Виды деятельности организации
    """
    try:
        organization = await OrganizationService(session=session).get_by_id(
            organization_id=organization_id,
        )
        return OrganizationDetailResponse.from_orm(organization)
    except OrganizationNotFoundById as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{organization_name}/detail_name/",
    response_model=OrganizationDetailResponse,
    summary="Получить организацию по названию",
    description="Возвращает полную информацию об организации по её точному названию",
    response_description="Детальная информация об организации включая контакты, адрес и виды деятельности",
)
async def get_organization_by_name(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    organization_name: str = Path(
        ..., description="Точное название организации", example="ООО Рога и Копыта"
    ),
):
    """
    Получение детальной информации об организации по названию.

    - **organization_name**: Полное точное название организации (регистрозависимый поиск)
    - **Возвращает**: Полную информацию об организации включая:
        - Основные данные (название, ID)
        - Контактные телефоны
        - Адрес здания с координатами
        - Виды деятельности организации

    **Примечание**: Поиск осуществляется по точному совпадению названия.
    """
    try:
        organization = await OrganizationService(session=session).get_by_name(
            organization_name=organization_name,
        )
        return OrganizationDetailResponse.from_orm(organization)
    except OrganizationNotFoundByName as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
