from typing import Any
import pytest
from faker import Faker
from contextlib import nullcontext as does_not_raise
from app.domain.values.name import Name, CountOfRequests, Probability
from app.domain.exceptions.name import (
    NameTooLongException,
    EmptyNameException,
    NegativeCountOfRequestsException,
    ProbabilityTooHighException,
    ProbabilityTooLowException,
)


class TestNameVT:
    @pytest.mark.parametrize(
        'name,expectation',
        [
            ('A', does_not_raise()),
            ('ValidName', does_not_raise()),
            ('A' * 85, does_not_raise()),
            ('', pytest.raises(EmptyNameException)),
            ('A' * 101, pytest.raises(NameTooLongException)),
        ],
    )
    def test_name_creation_param(self, name: str, expectation: Any):
        with expectation:
            assert Name(name).as_generic_type() == name

    def test_name_equality(self) -> None:

        name1 = Name('John')
        name2 = Name('John')
        name3 = Name('Jane')

        assert name1 == name2  # Same value
        assert name1 != name3  # Different value
        assert name1 != 'John'  # Different type


    def test_create_name(self, faker: Faker) -> None:
        name_length = faker.random_int(min=1, max=85)
        random_name = faker.pystr(min_chars=name_length, max_chars=name_length)
        name_value = Name(random_name)
        assert name_value.as_generic_type() == random_name


class TestCountOfRequestsVT:
    @pytest.mark.parametrize(
        'value,expectation',
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (100, does_not_raise()),
            (1000, does_not_raise()),
            (-1, pytest.raises(NegativeCountOfRequestsException)),
            (-100, pytest.raises(NegativeCountOfRequestsException)),
        ],
    )
    def test_count_of_requests_creation_param(self, value: int, expectation: Any):
        with expectation:
            assert CountOfRequests(value).as_generic_type() == value

    def test_count_of_requests_equality(self, faker: Faker) -> None:
        count1 = CountOfRequests(1)
        count2 = CountOfRequests(1)
        count3 = CountOfRequests(2)

        assert count1 == count2  # Same value
        assert count1 != count3  # Different value
        assert count1 != 1  # Different type

    def test_create_count_of_requests(self, faker: Faker) -> None:
        random_count = faker.random_int(min=0, max=1000)
        count_value = CountOfRequests(random_count)
        assert count_value.as_generic_type() == random_count


class TestProbabilityVT:
    @pytest.mark.parametrize(
        'value,expectation',
        [
            (0.0, does_not_raise()),
            (0.5, does_not_raise()),
            (0.999, does_not_raise()),
            (1.0, does_not_raise()),
            (1.1, pytest.raises(ProbabilityTooHighException)),
            (-0.1, pytest.raises(ProbabilityTooLowException)),
            (-1.0, pytest.raises(ProbabilityTooLowException)),
        ],
    )
    def test_probability_creation_param(self, value: float, expectation: Any):
        with expectation:
            assert Probability(value).as_generic_type() == value

    def test_probability_equality(self, faker: Faker) -> None:
        prob1 = Probability(0.5)
        prob2 = Probability(0.5)
        prob3 = Probability(0.6)

        assert prob1 == prob2  # Same value
        assert prob1 != prob3  # Different value
        assert prob1 != 0.5  # Different type


    def test_create_probability(self, faker: Faker) -> None:
        random_prob = faker.pyfloat(min_value=0.0, max_value=1.0)
        prob_value = Probability(random_prob)
        # Verify values
        assert prob_value.as_generic_type() == random_prob
