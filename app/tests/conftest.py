from punq import Container
from pytest import fixture

from infra.repositories.api.base import (
    BaseNameOriginAPIRepository,
    BaseCountryAPIRepository,
)
from logic.mediator import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope='function')
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(service_key=Mediator)


@fixture()
def name_origin_repository(container: Container) -> BaseNameOriginAPIRepository:
    return container.resolve(service_key=BaseNameOriginAPIRepository)


@fixture()
def country_repository(container: Container) -> BaseCountryAPIRepository:
    return container.resolve(service_key=BaseCountryAPIRepository)
