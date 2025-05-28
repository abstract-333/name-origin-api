from dataclasses import dataclass, field
from typing import Any, override
import httpx
from domain.entities.country import CountryEntity
from infra.repositories.api.base import BaseCountryAPIRepository


@dataclass
class CountriesAPIRepository(BaseCountryAPIRepository):
    """Implementation of BaseCountryRepository using the REST Countries API.

    This repository fetches country data from https://restcountries.com/v3.1/
    """

    base_url: str
    timeout: float = 5.0  # Default timeout of 5 seconds
    client: httpx.AsyncClient = field(init=False)

    def __post_init__(self):
        timeout = httpx.Timeout(self.timeout, connect=2.0)
        self.client = httpx.AsyncClient(timeout=timeout)

    @override
    async def get_list_of_countries(self) -> list[CountryEntity]:
        """Fetch all countries from the REST Countries API.

        Returns:
            list[CountryEntity]: A list of CountryEntity objects representing all countries.
        """
        try:
            response = await self.client.get(f'{self.base_url}/all')
            response.raise_for_status()

            countries_data = response.json()
            return [
                self._map_to_entity(country_data) for country_data in countries_data
            ]
        except httpx.HTTPStatusError as e:
            raise e

    @override
    async def get_country(self, name: str) -> CountryEntity | None:
        """Fetch a specific country by name from the REST Countries API.

        Args:
            name (str): The name of the country to retrieve (e.g., 'US' for United States).

        Returns:
            CountryEntity | None: The CountryEntity object if found, None otherwise.
        """
        try:
            response = await self.client.get(f'{self.base_url}/alpha/{name}')
            response.raise_for_status()

            countries_data = response.json()
            if not countries_data:
                return None

            return self._map_to_entity(countries_data[0])
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    @staticmethod
    def _map_to_entity(data: dict[str, Any]) -> CountryEntity:
        """Map REST Countries API response to CountryEntity.

        Args:
            data (dict[str, Any]): The country data from the API.

        Returns:
            CountryEntity: A CountryEntity object representing the country.
        """
        return CountryEntity(
            iso_alpha2_code=data['cca2'],
            common_name=data['name']['common'],
            official_name=data['name']['official'],
            region=data['region'],
            sub_region=data.get('subregion', ''),
            independent=data.get('independent', None),
            capital=set(data.get('capital', [])),
            capital_lat=data.get('capitalInfo', {}).get('latlng', [None, None])[0],
            capital_long=data.get('capitalInfo', {}).get('latlng', [None, None])[1],
            flag_png=data['flags']['png'],
            flag_svg=data['flags']['svg'],
            flag_alt=data['flags'].get('alt'),
            coat_of_arms_png=data.get('coatOfArms', {}).get('png'),
            coat_of_arms_svg=data.get('coatOfArms', {}).get('svg'),
            borders=set(data.get('borders', [])),
        )
