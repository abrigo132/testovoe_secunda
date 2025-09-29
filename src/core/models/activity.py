from sqlalchemy import CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import LtreeType
from typing import List, TYPE_CHECKING


from .m2m import organization_activities

from .base import Base
from core.models.mixins import IdIntPkMixin

if TYPE_CHECKING:
    from .organization import Organization


class Activity(IdIntPkMixin, Base):

    name: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column(LtreeType, nullable=False, index=True)
    level: Mapped[int] = mapped_column(default=0)

    organizations: Mapped[List["Organization"]] = relationship(
        secondary=organization_activities, back_populates="activities"
    )

    __table_args__ = (CheckConstraint("nlevel(path) <= 3", name="max_nesting_level_3"),)
