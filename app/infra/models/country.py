from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import String, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.models.base import Base

if TYPE_CHECKING:
    from infra.models.name import NameOriginModel


class CountryModel(Base):
    """SQLAlchemy model for storing country data."""

    __tablename__ = 'countries'

    iso_alpha2_code: Mapped[str] = mapped_column(String(2), primary_key=True)
    common_name: Mapped[str] = mapped_column(String(100))
    official_name: Mapped[str] = mapped_column(String(100))
    region: Mapped[str] = mapped_column(String(50))
    sub_region: Mapped[str] = mapped_column(String(50), nullable=True)
    independent: Mapped[bool] = mapped_column(Boolean, nullable=True)
    capital: Mapped[str] = mapped_column(String(100), nullable=True)
    capital_lat: Mapped[float] = mapped_column(Float, nullable=True)
    capital_long: Mapped[float] = mapped_column(Float, nullable=True)
    flag_png: Mapped[str] = mapped_column(String(200))
    flag_svg: Mapped[str] = mapped_column(String(200))
    flag_alt: Mapped[str] = mapped_column(String(200), nullable=True)
    coat_of_arms_png: Mapped[str] = mapped_column(String(200), nullable=True)
    coat_of_arms_svg: Mapped[str] = mapped_column(String(200), nullable=True)
    borders: Mapped[str] = mapped_column(
        String(200), nullable=True
    )  # Stored as comma-separated values
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    names: Mapped['NameOriginModel'] = relationship(
        'NameOriginModel', back_populates='country'
    )

    def __repr__(self) -> str:
        return f'<CountryModel(code={self.iso_alpha2_code}, name={self.common_name})>'
