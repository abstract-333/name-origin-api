from dataclasses import dataclass

from domain.entities.country import CountryEntity
from domain.entities.name import BaseNameEntity, NameEntity, NameStrEntity
from infra.repositories.base import BaseCountryRepository, BaseNameOriginRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.country import CountryNotFoundException
from logic.exceptions.name import NameNotFoundException


@dataclass(frozen=True)
class GetNameOriginsCommand(BaseCommand):
    name: str


@dataclass(frozen=True)
class GetNameOriginsCommandHandler(
    CommandHandler[GetNameOriginsCommand, set[NameEntity]]
):
    name_origin_repository: BaseNameOriginRepository
    country_repository: BaseCountryRepository

    async def handle(self, command: GetNameOriginsCommand) -> set[NameEntity]:
        name_origin: (
            set[BaseNameEntity] | None
        ) = await self.name_origin_repository.get_name_origins_probability(command.name)
        if not name_origin:
            raise NameNotFoundException(name=command.name)

        name_origins_with_country_entity: set[NameEntity] = set()

        for name_str_entity in name_origin:
            if not isinstance(name_str_entity, NameStrEntity):
                continue

            country_info: (
                CountryEntity | None
            ) = await self.country_repository.get_country(name_str_entity.country_name)
            if not country_info:
                raise CountryNotFoundException(
                    iso_alpha2_code=name_str_entity.country_name
                )

            name_entity = NameEntity(
                name=name_str_entity.name,
                count_of_requests=name_str_entity.count_of_requests,
                probability=name_str_entity.probability,
                country=country_info,
            )
            name_origins_with_country_entity.add(name_entity)
        return name_origins_with_country_entity
