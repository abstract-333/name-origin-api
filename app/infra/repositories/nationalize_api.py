import httpx
from domain.entities.name import NameStrEntity, BaseNameEntity
from domain.values.name import Name, Probability, CountOfRequests
from infra.repositories.base import BaseNameRepository


class NationalizeRepository(BaseNameRepository):
    """Implementation of BaseNameRepository using the Nationalize API.

    This repository fetches name nationality probability data from https://api.nationalize.io/
    """

    def __init__(self) -> None:
        self.base_url = 'https://api.nationalize.io'

    async def get_name_probability(self, name: str) -> set[BaseNameEntity] | None:
        """Fetch nationality probability for a given name from the Nationalize API.

        Args:
            name (str): The name to get nationality probability for.

        Returns:
            set[BaseNameEntity] | None: A set of BaseNameEntity objects containing probability information
                                      for each country if found, None otherwise.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f'{self.base_url}/?name={name}')
                response.raise_for_status()

                data = response.json()
                if not data.get('country'):
                    return None

                results: set[BaseNameEntity] = set()
                for country_data in data['country']:
                    results.add(
                        NameStrEntity(
                            name=Name(value=name),
                            probability=Probability(value=country_data['probability']),
                            count_of_requests=CountOfRequests(value=data['count']),
                            country_name=country_data['country_id'],
                        )
                    )

                return results if results else None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                return None
            raise
