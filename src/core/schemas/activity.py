from pydantic import BaseModel, ConfigDict, field_validator
from typing import List

from .base import OrganizationShort


class ActivityBase(BaseModel):
    name: str


class ActivityRead(ActivityBase):
    id: int
    path: str
    level: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("path", mode='before')
    @classmethod
    def convert_ltree(cls, v):
        if hasattr(v, 'val'):
            return v.val
        elif hasattr(v, 'value'):
            return v.value
        else:
            return str(v)


class ActivityWithOrganizationResponse(ActivityBase):
    id: int
    organizations: List["OrganizationShort"]
    max_level: int = 3

    model_config = ConfigDict(from_attributes=True)

# class ActivityTreeRead(ActivityRead):
#    children: List[ActivityTreeRead] = []


# ActivityTreeRead.model_rebuild()
ActivityWithOrganizationResponse.model_rebuild()
