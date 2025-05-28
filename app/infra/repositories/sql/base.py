from abc import abstractmethod, ABC
from dataclasses import dataclass

from domain.entities.country import CountryEntity
from domain.entities.name import NameEntity


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


@dataclass
class BaseNameRepository(ABC):
    """Abstract base class for name origin repository implementations.

    This class defines the interface for repositories that handle basic CRUD operations
    for name origin-related data. Concrete implementations must provide implementations
    for all abstract methods.
    """

    @abstractmethod
    async def get_name_origins(self, name: str) -> list[NameEntity] | None:
        """Retrieve name origins for a specific name.

        Args:
            name (str): The name to retrieve origins for.

        Returns:
            list[NameEntity] | None: List of NameEntity objects if found, None otherwise.
        """
        ...

    @abstractmethod
    async def get_frequent_names_by_country(self, country_name: str) -> list[NameEntity] | None:
        """Retrieve frequent names for a specific country.

        Args:
            country_name (str): The country name to retrieve frequent names for.

        Returns:
            list[NameEntity] | None: List of NameEntity objects if found, None otherwise.
        """
        ...

    @abstractmethod
    async def add_name_origin(self, name_origin: NameEntity) -> None:
        """Add a new name origin to the repository.

        Args:
            name_origin (NameEntity): The name origin entity to add.
        """
        ...
