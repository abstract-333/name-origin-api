from functools import lru_cache
from typing import Container
from punq import (
    Container,
    Scope,
)
from infra.repositories.base import BaseCountryRepository, BaseNameOriginRepository
from infra.repositories.countries_api import CountriesAPIRepository
from infra.repositories.nationalize_api import NationalizeRepository
from logic.commands.name import GetNameOriginsCommand, GetNameOriginsCommandHandler
from logic.mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    def init_nationalize_name_repository() -> BaseNameOriginRepository:
        return NationalizeRepository()

    def init_countries_api_repository() -> BaseCountryRepository:
        return CountriesAPIRepository()

    container.register(
        BaseNameOriginRepository,
        factory=init_nationalize_name_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseCountryRepository,
        factory=init_countries_api_repository,
        scope=Scope.singleton,
    )
    container.register(GetNameOriginsCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            GetNameOriginsCommand,
            [container.resolve(GetNameOriginsCommandHandler)],
        )
        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
