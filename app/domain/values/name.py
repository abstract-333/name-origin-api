from dataclasses import dataclass
from domain.exceptions.name import (
    EmptyNameException,
    NameTooLongException,
    ProbabilityTooHighException,
    ProbabilityTooLowException,
    NegativeCountOfRequestsException,
)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Name(BaseValueObject[str]):
    value: str

    """Value object for representing a name with validation.
    Attributes:
        value: The name string value
    """

    def validate(self) -> None:
        """Validate the name value."""
        if not self.value or not self.value.strip():
            raise EmptyNameException()

        if len(self.value) > 100:
            raise NameTooLongException(text=self.value, max_length=100)

    def as_generic_type(self) -> str:
        """Convert the name to a string.
        Returns:
            str: The name as a string
        """
        return str(object=self.value)


@dataclass(frozen=True)
class Probability(BaseValueObject[float]):
    """Value object for representing a probability with validation.
    Attributes:
        value: The probability value (must be between 0 and 1.0)
    """

    value: float

    def validate(self) -> None:
        """Validate the probability value."""
        if self.value > 1.0:
            raise ProbabilityTooHighException(probability=self.value)

        if self.value < 0:
            raise ProbabilityTooLowException(probability=self.value)

    def as_generic_type(self) -> float:
        """Convert the probability to a float.
        Returns:
            float: The probability as a float
        """
        return float(self.value)


@dataclass(frozen=True)
class CountOfRequests(BaseValueObject[int]):
    """Value object for representing count of requests with validation.

    Attributes:
        value: The count value (must be non-negative)
    """

    def validate(self) -> None:
        """Validate the count value."""
        if self.value < 0:
            raise NegativeCountOfRequestsException(count=self.value)

    def as_generic_type(self) -> int:
        """Convert the count to an integer.

        Returns:
            int: The count as an integer
        """
        return int(self.value)
