from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

from .base import Base
from core.models.mixins import IdIntPkMixin

if TYPE_CHECKING:
    from .organization import Organization


class PhoneNumber(IdIntPkMixin, Base):

    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="phone_numbers"
    )
