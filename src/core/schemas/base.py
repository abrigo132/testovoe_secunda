from pydantic import BaseModel, ConfigDict


class OrganizationShort(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class ActivityShort(BaseModel):
    id: int
    name: str
    path: str
    level: int
    model_config = ConfigDict(from_attributes=True)
