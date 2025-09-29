from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import GeoSearchResponse
from repositories import BuildingRepository
from core.exceptions import GeoSearchRadiusNotFoundOrganizations


class GeoSearchService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = BuildingRepository(session)

    async def search_organizations_in_radius(
        self, lat: float, lng: float, radius_km: float
    ) -> GeoSearchResponse:
        """
        Поиск организаций в радиусе от географической точки

        """

        # Ищем здания в радиусе
        buildings = await self.repo.get_buildings_in_radius(lat, lng, radius_km)

        if not buildings:
            raise GeoSearchRadiusNotFoundOrganizations(radius=radius_km)

        all_organizations = []
        for building in buildings:
            all_organizations.extend(building.organizations)

        unique_organizations = []
        seen_org_ids = set()

        for org in all_organizations:
            if org.id not in seen_org_ids:
                seen_org_ids.add(org.id)
                unique_organizations.append(org)

        return GeoSearchResponse(
            search_type="radius",
            organizations=unique_organizations,
            coordinates={"latitude": lat, "longitude": lng},
        )
