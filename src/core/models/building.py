from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geography
from typing import TYPE_CHECKING, List
from sqlalchemy import Index

from .base import Base
from core.models.mixins import IdIntPkMixin

if TYPE_CHECKING:
    from .organization import Organization


class Building(IdIntPkMixin, Base):

    address: Mapped[str] = mapped_column()
    coords: Mapped[Geography] = mapped_column(
        Geography(geometry_type="Point", srid=4326),
    )
    organizations: Mapped[List["Organization"]] = relationship(
        "Organization",
        back_populates="building",
    )

    __table_args__ = (
        Index("idx_buildings_coords_gist", "coords", postgresql_using="gist"),
    )
