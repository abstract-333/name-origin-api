from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities.country import CountryEntity
from domain.entities.name import BaseNameEntity


@dataclass
class BaseCountryRepository(ABC):
    """Abstract base class for country repository implementations.

    This class defines the interface for repositories that handle country-related data operations.
    Concrete implementations must provide implementations for all abstract methods.
    """

    @abstractmethod
    async def get_list_of_countries(self) -> set[CountryEntity]:
        """Retrieve a list of all available countries.

        Returns:
            set[CountryEntity]: A set of CountryEntity objects representing all available countries.
        """
        ...

    @abstractmethod
    async def get_country(self, name: str) -> CountryEntity | None:
        """Retrieve a specific country by its name.

        Args:
            name (str): The name of the country to retrieve.

        Returns:
            CountryEntity | None: The CountryEntity object if found, None otherwise.
        """
        ...


@dataclass
class BaseNameRepository(ABC):
    """Abstract base class for name repository implementations.

    This class defines the interface for repositories that handle name-related data operations,
    specifically for calculating name probabilities.
    """

    @abstractmethod
    async def get_name_probability(self, name: str) -> set[BaseNameEntity] | None:
        """Calculate and retrieve the probability information for a given name.

        Args:
            name (str): The name to calculate probability for.

        Returns:
            NameEntity | None: The NameEntity object containing probability information if found,
                             None otherwise.
        """
        ...
