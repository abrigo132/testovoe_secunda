from pydantic import BaseModel, Field
from typing import List, Optional


from .activity import ActivityRead
from .organization import OrganizationRead


class ActivityTreeSearchRequest(BaseModel):
    activity_path: str
    include_children: bool = True
    max_level: int = 3


class ActivityTreeSearchResponse(BaseModel):
    root_activity: ActivityRead
    included_activities: List["ActivityRead"]
    organizations: List["OrganizationRead"]


class GeoSearchRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Широта от -90 до 90")
    lng: float = Field(..., ge=-180, le=180, description="Долгота от -180 до 180")
    radius_km: float = Field(..., gt=0, description="Радиус поиска в километрах")


class CombinedSearchRequest(BaseModel):
    activity_path: Optional[str] = None
    building_id: Optional[int] = None
    name: Optional[str] = None
    geo_search: Optional["GeoSearchRequest"] = None


class GeoSearchResponse(BaseModel):
    search_type: str
    coordinates: dict
    organizations: List["OrganizationRead"]
