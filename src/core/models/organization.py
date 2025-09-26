from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

from .base import Base
from core.models.mixins import IdIntPkMixin
from .m2m import organization_activities

if TYPE_CHECKING:
    from .phone_number import PhoneNumber
    from .building import Building
    from .activity import Activity


class Organization(IdIntPkMixin, Base):

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_numbers: Mapped[List["PhoneNumber"]] = relationship(
        "PhoneNumber", back_populates="organization"
    )
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    building: Mapped["Building"] = relationship(
        "Building", back_populates="organizations"
    )

    activities: Mapped[List["Activity"]] = relationship(
        secondary=organization_activities, back_populates="organizations"
    )
