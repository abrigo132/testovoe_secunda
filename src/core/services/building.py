from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Building
from repositories import BuildingRepository
from core.exceptions import BuildingNotFound


class BuildingService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.building_repository = BuildingRepository(self.session)

    async def get_building_by_id(self, building_id: int) -> Building:
        building: Building | None = await self.building_repository.get(
            building_id=building_id
        )

        if building is None:
            raise BuildingNotFound(building_id)

        return building
