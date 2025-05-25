from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class NameNotFoundException(LogicException):
    name: str

    @property
    def message(self) -> str:
        return f'Any details about name "{self.name}" not found'
