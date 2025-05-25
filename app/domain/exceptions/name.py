from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class NameTooLongException(ApplicationException):
    text: str
    max_length: int

    @property
    def message(self) -> str:
        return f'Length of name is too long {self.text[: self.max_length]}...'


@dataclass(eq=False)
class EmptyNameException(ApplicationException):
    @property
    def message(self) -> str:
        return "Name can't be empty"


@dataclass(eq=False)
class ProbabilityTooHighException(ApplicationException):
    probability: float

    @property
    def message(self) -> str:
        return f'Probability {self.probability} is too high. Maximum allowed is 1.0'


@dataclass(eq=False)
class ProbabilityTooLowException(ApplicationException):
    probability: float

    @property
    def message(self) -> str:
        return f'Probability {self.probability} is too low. Minimum allowed is 0.0'


@dataclass(eq=False)
class NegativeCountOfRequestsException(ApplicationException):
    count: int

    @property
    def message(self) -> str:
        return f'Count of requests {self.count} cannot be negative'
