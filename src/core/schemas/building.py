from pydantic import BaseModel, field_validator, ConfigDict
from typing import List, Tuple

from .base import OrganizationShort


coords_fields = ["coords", "lat", "lng"]


class BuildingBase(BaseModel):
    address: str


class BuildingRead(BuildingBase):
    id: int
    coords: Tuple[float, float]

    @field_validator("coords", mode="before")
    @classmethod
    def convert_geography(cls, v) -> Tuple[float, float]:
        if hasattr(v, "x") and hasattr(v, "y"):
            return float(v.x), float(v.y)
        return v


class BuildingWithOrganizationResponse(BaseModel):
    building: BuildingRead
    organizations: List["OrganizationShort"]

    model_config = ConfigDict(from_attributes=True)
