from fastapi import APIRouter, Depends, status, Path
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
    summary="Получить организации в здании",
    description="Возвращает информацию о здании и список всех организаций, расположенных в нём",
    response_description="Информация о здании и список организаций",
)
async def get_organizations_in_building(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    building_id: int = Path(
        ..., description="Уникальный идентификатор здания", example=1
    ),
):
    """
    Получение списка организаций, расположенных в конкретном здании.

    - **building_id**: Уникальный числовой идентификатор здания в системе
    - **Возвращает**: Объект содержащий:
        - Информацию о здании (адрес, координаты, ID)
        - Список организаций в этом здании с их основными данными

    **Пример использования**:
    - Запрос к `/api/v1/buildings/1/organizations/` вернет все организации, расположенные в здании с ID=1
    """
    try:
        building = await BuildingService(session=session).get_building_by_id(
            building_id=building_id,
        )
        return BuildingWithOrganizationResponse.model_validate(
            building, from_attributes=True
        )
    except BuildingNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
