from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, Sequence
from sqlalchemy import select, ScalarResult
from sqlalchemy.orm import selectinload
from geoalchemy2 import functions as gis_func

from core.models import Building


class BuildingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model: Type[Building] = Building

    async def get(self, building_id: int) -> Building | None:
        stmt = (
            select(self.model)
            .where(self.model.id == building_id)
            .options(selectinload(self.model.organizations))
        )
        scalar_result: ScalarResult[Building] = await self.session.scalars(stmt)
        return scalar_result.one_or_none()

    async def get_buildings_in_radius(
        self,
        lat: float,
        lng: float,
        radius_km: float,
    ) -> Sequence[Building]:
        radius_meters = radius_km * 1000

        point = gis_func.ST_SetSRID(gis_func.ST_MakePoint(lat, lng), 4326)

        stmt = (
            select(self.model)
            .where(gis_func.ST_DWithin(self.model.coords, point, radius_meters))
            .options(
                selectinload(self.model.organizations).options(
                    selectinload(self.model.organizations.phone_numbers),
                    selectinload(self.model.organizations.activities),
                )
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
