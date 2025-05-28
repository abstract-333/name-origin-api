from dataclasses import dataclass

from domain.entities.country import CountryEntity
from domain.entities.name import BaseNameEntity, NameEntity, NameStrEntity
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
    unit_of_work: IUnitOfWork

    async def handle(self, command: GetNameOriginsCommand) -> list[NameEntity]:
        name_origin: (
            list[BaseNameEntity] | None
        ) = await self.name_origin_api_repository.get_name_origins_probability(
            command.name
        )
        if not name_origin:
            raise NameNotFoundException(name=command.name)

        name_origins_with_country_entity: list[NameEntity] = []

        for name_str_entity in name_origin:
            if not isinstance(name_str_entity, NameStrEntity):
                continue
            country_info:  CountryEntity | None
            async with self.unit_of_work:
            # Try SQL repository first
                country_info = await self.unit_of_work.country.get_country(
                name_str_entity.country_name
            )

            # If not found in SQL, try API and cache the result
            async with self.unit_of_work:
                if not country_info:
                    country_info = await self.country_api_repository.get_country(
                        name_str_entity.country_name
                    )
                    if not country_info:
                        raise CountryNotFoundException(
                            iso_alpha2_code=name_str_entity.country_name
                        )
                    # Cache the country in SQL repository
                    await self.unit_of_work.country.add_country(country_info)
                    await self.unit_of_work.commit()

            name_entity = NameEntity(
                name=name_str_entity.name,
                count_of_requests=name_str_entity.count_of_requests,
                probability=name_str_entity.probability,
                country=country_info,
            )
            name_origins_with_country_entity.append(name_entity)
        return sorted(
            name_origins_with_country_entity,
            key=lambda x: x.probability.as_generic_type(),
            reverse=True,
        )
