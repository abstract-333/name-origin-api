from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.models.base import Base

if TYPE_CHECKING:
    from infra.models.country import CountryModel


class NameOriginModel(Base):
    """SQLAlchemy model for storing name origin data."""

    __tablename__ = 'names_origin'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    probability: Mapped[float] = mapped_column(Float)
    count_of_requests: Mapped[int] = mapped_column(Integer)
    country_code: Mapped[str] = mapped_column(
        String(2), ForeignKey('countries.iso_alpha2_code')
    )
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    last_accessed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    country: Mapped['CountryModel'] = relationship(back_populates='names')

    def __repr__(self) -> str:
        return f'<NameModel(name={self.name}, country={self.country_code}, probability={self.probability})>'
