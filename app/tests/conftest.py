from punq import Container
from pytest import fixture

from infra.repositories.base import BaseNameOriginRepository, BaseCountryRepository
from logic.mediator import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope='function')
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(service_key=Mediator)


@fixture()
def name_origin_repository(container: Container) -> BaseNameOriginRepository:
    return container.resolve(service_key=BaseNameOriginRepository)


@fixture()
def country_repository(container: Container) -> BaseCountryRepository:
    return container.resolve(service_key=BaseCountryRepository)
