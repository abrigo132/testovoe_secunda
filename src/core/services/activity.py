from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import Ltree

from core.models import Activity, Organization
from repositories import ActivityRepository
from core.exceptions import ActivityNotFound, ActivityNotFoundPathTree


class ActivityService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.activity_repo = ActivityRepository(session)

    async def get_activity_by_name_with_organizations(
        self, activity_name: str
    ) -> Activity:
        activity = await self.activity_repo.get(activity_name=activity_name)

        if activity is None:
            raise ActivityNotFound(activity_name)
        return activity

    async def search_organizations_by_activity_tree(
        self, activity_path: str
    ) -> Sequence[Organization]:
        ltree_path = Ltree(activity_path)
        organizations = await self.activity_repo.get_organizations_by_activity_tree(
            ltree_path
        )

        if not organizations:
            raise ActivityNotFoundPathTree(activity_path)

        return organizations
