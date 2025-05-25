from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class CountryNotFoundException(LogicException):
    iso_alpha2_code: str

    @property
    def message(self) -> str:
        return f'Country with code "{self.iso_alpha2_code}" not found'
