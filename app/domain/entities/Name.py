from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID
from uuid_utils import uuid7
from domain.entities.country import CountryEntity
from domain.values.name import CountOfRequests, Name, Probability


@dataclass
class BaseNameEntity:
    """Name entity for storing name-related data.
    Attributes:
        id: Unique identifier using UUID-7
        name: The name to be analyzed (max 85 characters)
        count_of_requests: Number of represented rows of the name
        last_accessed: UTC timestamp of the last request
        probability: Probability score for the name's country association
    """

    id: UUID = field(
        default_factory=uuid7,
    )
    name: Name = field(
        kw_only=True,
    )
    count_of_requests: CountOfRequests = field(
        kw_only=True,
    )
    last_accessed: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        kw_only=True,
    )
    probability: Probability = field(
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, BaseNameEntity):
            raise NotImplementedError

        return self.id == __value.id


@dataclass(eq=False)
class NameEntity(BaseNameEntity):
    """Concrete implementation of BaseNameEntity that uses CountryEntity for country information.

    This entity stores the full country information as a CountryEntity object, providing
    access to all country-related data and functionality.
    """

    country: CountryEntity = field(
        kw_only=True,
    )


@dataclass(eq=False)
class NameStrEntity(BaseNameEntity):
    """Concrete implementation of BaseNameEntity that uses string for country information.

    This entity stores only the country name as a string, providing a simpler representation
    when only the country name is needed without the full country entity data.
    """

    country_name: str = field(
        kw_only=True,
    )
