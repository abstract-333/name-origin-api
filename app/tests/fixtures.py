from punq import (
    Container,
)

from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    return container
