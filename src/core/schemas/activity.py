from pydantic import BaseModel
from typing import List

from .base import OrganizationShort


class ActivityBase(BaseModel):
    name: str


class ActivityRead(ActivityBase):
    id: int
    path: str
    level: int

    class Config:
        from_attributes = True


class ActivityWithOrganizationResponse(ActivityBase):
    id: int
    organizations: List["OrganizationShort"]
    max_level: int = 3


# class ActivityTreeRead(ActivityRead):
#    children: List[ActivityTreeRead] = []


# ActivityTreeRead.model_rebuild()
ActivityWithOrganizationResponse.model_rebuild()
