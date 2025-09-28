from pydantic import BaseModel
from typing import List


from .building import BuildingRead
from .activity import ActivityRead


class PhoneNumber(BaseModel):
    phone_number: str


class OrganizationBase(BaseModel):
    name: str


class OrganizationRead(BaseModel):
    id: int
    name: str
    phone_numbers: List[PhoneNumber]
    building: "BuildingRead"
    activities: List["ActivityRead"]

    class Config:
        from_attributes = True


class OrganizationSearchRequest(OrganizationBase):
    limit: int = 50


class OrganizationSearchResponse(BaseModel):
    organizations: List["OrganizationRead"]


class OrganizationDetailResponse(OrganizationRead):
    pass


OrganizationDetailResponse.model_rebuild()
