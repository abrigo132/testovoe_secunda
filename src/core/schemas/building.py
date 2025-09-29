from pydantic import BaseModel, field_validator, ConfigDict, model_validator, BeforeValidator
from typing import List, Tuple
from geoalchemy2.shape import to_shape


from .base import OrganizationShort


coords_fields = ["coords", "lat", "lng"]


class BuildingBase(BaseModel):
    address: str


class BuildingRead(BuildingBase):
    id: int
    coords: Tuple[float, float]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("coords", mode="before")
    @classmethod
    def validate(cls, v):
        geom = to_shape(v)
        return geom.x, geom.y


class BuildingWithOrganizationResponse(BuildingRead):
    organizations: List["OrganizationShort"]

    model_config = ConfigDict(from_attributes=True)
