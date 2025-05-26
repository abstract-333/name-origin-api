from functools import lru_cache
from collections.abc import Container
from punq import (
    Container,
    Scope,
)
from infra.repositories.base import BaseCountryAPIRepository, BaseNameOriginAPIRepository
from infra.repositories.countries_api import CountriesAPIRepository
from infra.repositories.nationalize_api import NationalizeRepository
from infra.repositories.session_generator import SessionGenerator
from logic.commands.name import GetNameOriginsCommand, GetNameOriginsCommandHandler
from logic.mediator import Mediator
from settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    def create_async_session() -> SessionGenerator:
        return SessionGenerator(
            db_url=config.postgres_url,
            debug=config.debug,
        )
    
    container.register(
        SessionGenerator,
        factory=create_async_session,
        scope=Scope.singleton,
    )
    session = container.resolve(SessionGenerator)
    
    def init_nationalize_name_repository() -> BaseNameOriginAPIRepository:
        return NationalizeRepository(base_url=config.nationalize_api_url)

    def init_countries_api_repository() -> BaseCountryAPIRepository:
        return CountriesAPIRepository(base_url=config.rest_countries_api_url)

    container.register(
        BaseNameOriginAPIRepository,
        factory=init_nationalize_name_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseCountryAPIRepository,
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
