from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
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
    "/{activity_name}/organizations/",
    response_model=ActivityWithOrganizationResponse,
    summary="Получить деятельность с организациями",
    description="Возвращает информацию о виде деятельности и список всех организаций, связанных с этой деятельностью",
    response_description="Информация о виде деятельности и список связанных организаций",
)
async def get_activity_with_organizations(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    activity_name: str = Path(
        ..., description="Название вида деятельности", example="ресторан"
    ),
):
    """
    Получение информации о конкретном виде деятельности и организаций, которые ей занимаются.

    - **activity_name**: Название вида деятельности (точное совпадение)
    - **Возвращает**: Объект содержащий:
        - Информацию о виде деятельности (название, путь, уровень)
        - Список организаций, занимающихся этой деятельностью

    **Примечание**: Поиск осуществляется по точному названию деятельности.
    **Пример**: Запрос к `/api/v1/activities/ресторан/organizations/` вернет
    вид деятельности "ресторан" и все организации с этой деятельностью.
    """
    try:
        activity = await ActivityService(
            session=session
        ).get_activity_by_name_with_organizations(
            activity_name=activity_name,
        )
        return ActivityWithOrganizationResponse.model_validate(activity)

    except ActivityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{activity_path:path}/search/organizations/",
    response_model=List[OrganizationShort],
    summary="Поиск организаций по дереву деятельностей",
    description="Рекурсивный поиск организаций по всему поддереву видов деятельности",
    response_description="Список организаций, связанных с указанным видом деятельности и всеми его подкатегориями",
)
async def search_organizations_by_activity_tree(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    activity_path: str = Path(
        ..., description="Путь в дереве деятельностей", example="food/food.meat"
    ),
):
    """
    Рекурсивный поиск организаций по дереву видов деятельности.

    - **activity_path**: Путь в иерархии деятельностей (регистрозависимый)
    - **Возвращает**: Список организаций, которые занимаются:
        - Указанным видом деятельности
        - Любым из его подкатегорий (рекурсивно по всему дереву)

    **Особенности поиска**:
    - Поиск осуществляется по всему поддереву указанной деятельности
    - Используется Ltree для эффективного поиска в иерархии
    - Максимальная глубина вложенности - 3 уровня

    **Примеры**:
    - `/api/v1/activities/еда/search/organizations/` найдет организации для:
      "Еда", "Еда.Мясная_продукция", "Еда.Молочная_продукция", "Еда.Рестораны" и т.д.
    - `/api/v1/activities/еда.рестораны/search/organizations/` найдет организации для:
      "Еда.Рестораны", "Еда.Рестораны.Фастфуд", "Еда.Рестораны.Кафе" и т.д.
    """
    try:
        organizations = await ActivityService(
            session=session
        ).search_organizations_by_activity_tree(activity_path)
        return [OrganizationShort.model_validate(org) for org in organizations]
    except ActivityNotFoundPathTree as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
