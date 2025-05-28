from dataclasses import dataclass

from domain.entities.country import CountryEntity
from domain.entities.name import NameEntity, NameStrEntity
from infra.repositories.api.base import (
    BaseCountryAPIRepository,
    BaseNameOriginAPIRepository,
)
from infra.repositories.sql.unit_of_work import IUnitOfWork
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.country import CountryNotFoundException
from logic.exceptions.name import NameNotFoundException


@dataclass(frozen=True)
class GetNameOriginsCommand(BaseCommand):
    name: str


@dataclass(frozen=True)
class GetNameOriginsCommandHandler(
    CommandHandler[GetNameOriginsCommand, list[NameEntity]]
):
    name_origin_api_repository: BaseNameOriginAPIRepository
    country_api_repository: BaseCountryAPIRepository
    uow: IUnitOfWork

    async def handle(self, command: GetNameOriginsCommand) -> list[NameEntity]:
        name_origins: list[NameEntity] | None = await self._get_names_origins_db(
            command.name
        )
        if name_origins:
            return name_origins

        name_origins_from_api: (
            list[NameStrEntity] | None
        ) = await self.name_origin_api_repository.get_name_origins(name=command.name)
        if not name_origins_from_api:
            raise NameNotFoundException(name=command.name)

        name_origins_with_country_entity: list[NameEntity] = []

        for name_str_entity in name_origins_from_api:
            country_info: CountryEntity | None = await self._get_country_info_db(
                name=name_str_entity.country_name
            )

            # If not found in SQL, try API and cache the result
            if not country_info:
                country_info = await self.country_api_repository.get_country(
                    name_str_entity.country_name
                )
                if not country_info:
                    raise CountryNotFoundException(
                        iso_alpha2_code=name_str_entity.country_name
                    )
                await self._save_country_to_db(country_info)

            name_entity = NameEntity(
                name=name_str_entity.name,
                count_of_requests=name_str_entity.count_of_requests,
                probability=name_str_entity.probability,
                country=country_info,
            )
            await self._save_name_to_db(name_entity=name_entity)

            name_origins_with_country_entity.append(name_entity)

        return sorted(
            name_origins_with_country_entity,
            key=lambda x: x.probability.as_generic_type(),
            reverse=True,
        )

    async def _save_country_to_db(self, country_info: CountryEntity) -> None:
        """Save country information to the database.

        Args:
            country_info (CountryEntity): The country entity to save.
        """
        async with self.uow:
            await self.uow.country.add_country(country_info)
            await self.uow.commit()

        return None

    async def _save_name_to_db(self, name_entity: NameEntity) -> None:
        """Save name information to the database.

        Args:
            name (NameEntity): The country entity to save.
        """
        async with self.uow:
            await self.uow.name.add_name_origin(name_origin=name_entity)
            await self.uow.commit()

        return None

    async def _get_country_info_db(self, name: str) -> CountryEntity | None:
        """Get country information from SQL repository.

        Args:
            name (str): The country name to fetch.

        Returns:
            CountryEntity | None: The country entity if found, None otherwise.
        """
        async with self.uow:
            country_info: CountryEntity | None = await self.uow.country.get_country(
                name
            )
            return country_info

    async def _get_names_origins_db(self, name: str) -> list[NameEntity] | None:
        """Get name origins from UoW repository.

        Args:
            name (str): The name to fetch origins for.

        Returns:
            list[BaseNameEntity] | None: List of name entities if found, None otherwise.
        """
        async with self.uow:
            return await self.uow.name.get_name_origins(name=name)


@dataclass(frozen=True)
class GetFrequentNamesCountryCommand(BaseCommand):
    country_name: str


@dataclass(frozen=True)
class GetFrequentNamesCountryCommandHandler(
    CommandHandler[GetFrequentNamesCountryCommand, list[NameEntity] | None]
):
    uow: IUnitOfWork

    async def handle(self, command: GetFrequentNamesCountryCommand) -> list[NameEntity] | None:
        async with self.uow:
            names:  list[NameEntity] | None = await self.uow.name.get_frequent_names_by_country(command.country_name) 
            return names