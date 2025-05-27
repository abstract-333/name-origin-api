from abc import abstractmethod, ABC
from dataclasses import dataclass

from domain.entities.country import CountryEntity


@dataclass
class BaseCountryRepository(ABC):
    """Abstract base class for country repository implementations.

    This class defines the interface for repositories that handle basic CRUD operations
    for country-related data. Concrete implementations must provide implementations
    for all abstract methods.
    """

    @abstractmethod
    async def get_country(self, name: str) -> CountryEntity | None:
        """Retrieve a specific country by its name.

        Args:
            name (str): The name of the country to retrieve.

        Returns:
            CountryEntity | None: The CountryEntity object if found, None otherwise.
        """
        ...

    @abstractmethod
    async def add_country(self, country: CountryEntity) -> CountryEntity:
        """Add a new country to the repository.

        Args:
            country (CountryEntity): The country entity to add.

        Returns:
            CountryEntity: The added country entity.
        """
        ...

    @abstractmethod
    async def delete_country(self, name: str) -> None:
        """Delete a country by its name.

        Args:
            name (str): The name of the country to delete.
        """
        ...

    @abstractmethod
    async def update_country(
        self, name: str, country: CountryEntity
    ) -> CountryEntity | None:
        """Update a country by its name.

        Args:
            name (str): The name of the country to update.
            country (CountryEntity): The updated country data.

        Returns:
            CountryEntity | None: The updated country entity if successful, None otherwise.
        """
        ...
