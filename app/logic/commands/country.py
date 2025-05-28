from dataclasses import dataclass
from infra.repositories.api.base import BaseCountryAPIRepository
from infra.repositories.sql.unit_of_work import IUnitOfWork
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class FetchAndSaveCountriesCommand(BaseCommand):
    """Command to fetch all countries from API and save them to database."""

    pass


@dataclass(frozen=True)
class FetchAndSaveCountriesCommandHandler(
    CommandHandler[FetchAndSaveCountriesCommand, None]
):
    """Handler for FetchAndSaveCountriesCommand.

    This handler:
    1. Fetches all countries from the API
    2. Saves them to the database
    3. Returns the list of saved countries
    """

    country_api_repository: BaseCountryAPIRepository
    uow: IUnitOfWork

    async def handle(self, command: FetchAndSaveCountriesCommand) -> None:
        # Fetch all countries from API
        countries = await self.country_api_repository.get_list_of_countries()

        # Save all countries to database
        async with self.uow:
            for country in countries:
                await self.uow.country.add_country(country)
            else:
                await self.uow.commit()
        return None
