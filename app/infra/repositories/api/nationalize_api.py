from dataclasses import dataclass, field
from typing import override
import httpx
import time
from domain.entities.name import NameStrEntity, BaseNameEntity
from domain.values.name import Name, Probability, CountOfRequests
from infra.repositories.api.base import BaseNameOriginAPIRepository


@dataclass
class NationalizeRepository(BaseNameOriginAPIRepository):
    """Implementation of BaseNameRepository using the Nationalize API.

    This repository fetches name nationality probability data from https://api.nationalize.io/
    """

    base_url: str
    timeout: float = 5.0  # Default timeout of 5 seconds
    client: httpx.AsyncClient = field(init=False)

    def __post_init__(self):
        timeout = httpx.Timeout(self.timeout, connect=2.0)
        self.client = httpx.AsyncClient(timeout=timeout)

    @override
    async def get_name_origins_probability(
        self, name: str
    ) -> list[BaseNameEntity] | None:
        """Fetch nationality probability for a given name from the Nationalize API.

        Args:
            name (str): The name to get nationality probability for.

        Returns:
            list[BaseNameEntity] | None: A list of BaseNameEntity objects containing probability information
                                      for each country if found, None otherwise.
        """
        start_time = time.time()
        try:
            response = await self.client.get(f'{self.base_url}/?name={name}')
            response.raise_for_status()

            data = response.json()
            duration = time.time() - start_time
            print(f'GET {self.base_url}/?name={name} took {duration:.3f} seconds')

            if not data.get('country'):
                return None

            results: list[BaseNameEntity] = []
            for country_data in data['country']:
                results.append(
                    NameStrEntity(
                        name=Name(value=name),
                        probability=Probability(value=country_data['probability']),
                        count_of_requests=CountOfRequests(value=data['count']),
                        country_name=country_data['country_id'],
                    )
                )

            return results if results else None
        except httpx.HTTPStatusError as e:
            duration = time.time() - start_time
            print(
                f'GET {self.base_url}/?name={name} failed after {duration:.3f} seconds'
            )
            if e.response.status_code == 400:
                return None
            raise
