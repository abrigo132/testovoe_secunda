from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Organization
from repositories import OrganizationRepository
from core.exceptions import OrganizationNotFoundById, OrganizationNotFoundByName


class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.organization_repo = OrganizationRepository(self.session)

    async def get_by_id(self, organization_id: int) -> Organization:
        organization: Organization | None = await self.organization_repo.get_by_id(
            organization_id=organization_id,
        )

        if organization is None:
            raise OrganizationNotFoundById(organization_id)

        return organization

    async def get_by_name(self, organization_name: str) -> Organization:
        organization: Organization | None = await self.organization_repo.get_by_name(
            organization_name=organization_name,
        )

        if organization is None:
            raise OrganizationNotFoundByName(organization_name)

        return organization
