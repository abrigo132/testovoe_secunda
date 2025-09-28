from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from typing import Type, Sequence

from core.models import Activity, Organization


class ActivityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.activity_model: Type[Activity] = Activity
        self.organizations_model: Type[Organization] = Organization

    async def get(self, activity_name: str) -> Activity | None:
        stmt = (
            select(self.activity_model)
            .where(self.activity_model.name == activity_name)
            .options(selectinload(self.activity_model.organizations))
        )
        scalar_result: ScalarResult[Activity] = await self.session.scalars(stmt)
        return scalar_result.unique().one_or_none()

    async def get_organizations_by_activity_tree(
        self, activity_path: str
    ) -> Sequence[Organization]:
        stmt = (
            select(self.organizations_model)
            .join(self.organizations_model.activities)
            .where(self.activity_model.path.op("<@")(activity_path))
            .options(
                selectinload(self.organizations_model.phone_numbers),
                joinedload(self.organizations_model.building),
            )
            .distinct()
        )

        result = await self.session.execute(stmt)
        return result.unique().scalars().all()
