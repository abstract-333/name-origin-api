from functools import lru_cache
from collections.abc import Container

from punq import (
    Container,
    Scope,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infra.repositories.api.base import (
    BaseCountryAPIRepository,
    BaseNameOriginAPIRepository,
)
from infra.repositories.api.countries_api import CountriesAPIRepository
from infra.repositories.api.nationalize_api import NationalizeRepository
from infra.repositories.sql.session_generator import (
    AsyncSessionFactory,
)
from infra.repositories.sql.unit_of_work import UnitOfWork, IUnitOfWork
from logic.commands.country import (
    FetchAndSaveCountriesCommand,
    FetchAndSaveCountriesCommandHandler,
)
from logic.commands.name import (
    GetFrequentNamesCountryCommand,
    GetFrequentNamesCountryCommandHandler,
    GetNameOriginsCommand,
    GetNameOriginsCommandHandler,
)
from logic.mediator import Mediator
from settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    def create_session_maker() -> async_sessionmaker[AsyncSession]:
        return AsyncSessionFactory(
            url=config.postgres_url,
            debug=config.debug,
        ).get_async_session_maker()

    container.register(
        async_sessionmaker[AsyncSession],
        factory=create_session_maker,
        scope=Scope.singleton,
    )
    session_maker = container.resolve(async_sessionmaker[AsyncSession])

    def init_unit_of_work() -> IUnitOfWork:
        return UnitOfWork(
            session_factory=session_maker,
        )

    container.register(
        IUnitOfWork,
        factory=init_unit_of_work,
        scope=Scope.singleton,
    )

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
    container.register(FetchAndSaveCountriesCommandHandler)
    container.register(GetFrequentNamesCountryCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            GetNameOriginsCommand,
            [container.resolve(GetNameOriginsCommandHandler)],
        )
        mediator.register_command(
            FetchAndSaveCountriesCommand,
            [container.resolve(FetchAndSaveCountriesCommandHandler)],
        )
        mediator.register_command(
            GetFrequentNamesCountryCommand,
            [container.resolve(GetFrequentNamesCountryCommandHandler)],
        )
        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
