from pydantic import BaseModel, ConfigDict
from typing import List


from .building import BuildingRead
from .activity import ActivityRead


class PhoneNumber(BaseModel):
    phone_number: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationBase(BaseModel):
    name: str


class OrganizationRead(BaseModel):
    id: int
    name: str
    phone_numbers: List[PhoneNumber]
    building: "BuildingRead"
    activities: List["ActivityRead"]

    model_config = ConfigDict(from_attributes=True)


class OrganizationSearchRequest(OrganizationBase):
    limit: int = 50


class OrganizationSearchResponse(BaseModel):
    organizations: List["OrganizationRead"]


class OrganizationDetailResponse(OrganizationRead):

    @classmethod
    def from_orm(cls, org_obj):
        return cls(
            id=org_obj.id,
            name=org_obj.name,
            phone_numbers=[PhoneNumber.model_validate(pn) for pn in org_obj.phone_numbers],
            building=BuildingRead.model_validate(org_obj.building),
            activities=[ActivityRead.model_validate(act) for act in org_obj.activities]
        )


OrganizationDetailResponse.model_rebuild()
