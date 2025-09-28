from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, ScalarResult
from sqlalchemy.orm import joinedload, selectinload

from core.models import Organization


class OrganizationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Organization

    async def get_by_id(
        self,
        organization_id: int,
    ) -> Organization | None:
        stmt = (
            select(self.model)
            .where(self.model.id == organization_id)
            .options(*self._get_loading_options())
        )
        result: ScalarResult[Organization] = await self.session.scalars(stmt)
        return result.unique().one_or_none()

    async def get_by_name(
        self,
        organization_name: str,
    ) -> Organization | None:
        stmt = (
            select(self.model)
            .where(self.model.name == organization_name)
            .options(*self._get_loading_options())
        )
        result: ScalarResult[Organization] = await self.session.scalars(stmt)
        return result.unique().one_or_none()

    def _get_loading_options(self):
        """Общие опции загрузки связей"""
        return (
            joinedload(self.model.building),
            selectinload(self.model.phone_numbers),
            selectinload(self.model.activities),
        )
