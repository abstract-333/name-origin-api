from datetime import datetime, UTC
from app.domain.entities.name import BaseNameEntity, NameEntity, NameStrEntity
from app.domain.entities.country import CountryEntity
from app.domain.values.name import CountOfRequests, Name, Probability


def test_base_name_entity_creation() -> None:
    name_entity = BaseNameEntity(
        name=Name('John'),
        count_of_requests=CountOfRequests(1),
        probability=Probability(0.85),
    )

    assert name_entity.name.as_generic_type() == Name('John').as_generic_type()
    assert (
        name_entity.count_of_requests.as_generic_type()
        == CountOfRequests(1).as_generic_type()
    )
    assert (
        name_entity.probability.as_generic_type() == Probability(0.85).as_generic_type()
    )
    assert isinstance(name_entity.last_accessed, datetime)
    assert name_entity.last_accessed.tzinfo == UTC


def test_name_entity_creation() -> None:
    country = CountryEntity(
        iso_alpha2_code='US',
        common_name='United States',
        official_name='United States of America',
        region='Americas',
        sub_region='North America',
        independent=True,
        capital={'Washington, D.C.'},
        capital_lat=38.8951,
        capital_long=-77.0364,
        flag_png='https://flagcdn.com/w320/us.png',
        flag_svg='https://flagcdn.com/us.svg',
        flag_alt='The flag of the United States of America',
        coat_of_arms_png='https://mainfacts.com/media/images/coats_of_arms/us.png',
        coat_of_arms_svg='https://mainfacts.com/media/images/coats_of_arms/us.svg',
        borders={'CAN', 'MEX'},
    )

    name_entity = NameEntity(
        name=Name('John'),
        count_of_requests=CountOfRequests(1),
        probability=Probability(0.85),
        country=country,
    )

    assert (
        name_entity.count_of_requests.as_generic_type()
        == CountOfRequests(1).as_generic_type()
    )
    assert (
        name_entity.probability.as_generic_type() == Probability(0.85).as_generic_type()
    )
    assert isinstance(name_entity.last_accessed, datetime)
    assert name_entity.last_accessed.tzinfo == UTC
    assert name_entity.country == country


def test_name_str_entity_creation() -> None:
    name_entity = NameStrEntity(
        name=Name('John'),
        count_of_requests=CountOfRequests(1),
        probability=Probability(0.85),
        country_name='United States',
    )

    assert name_entity.name.as_generic_type() == Name('John').as_generic_type()
    assert (
        name_entity.count_of_requests.as_generic_type()
        == CountOfRequests(1).as_generic_type()
    )
    assert (
        name_entity.probability.as_generic_type() == Probability(0.85).as_generic_type()
    )
    assert isinstance(name_entity.last_accessed, datetime)
    assert name_entity.last_accessed.tzinfo == UTC
    assert name_entity.country_name == 'United States'


def test_base_name_entity_hash_and_eq() -> None:
    entity1 = BaseNameEntity(
        name=Name('John'),
        count_of_requests=CountOfRequests(1),
        probability=Probability(0.85),
    )
    entity2 = BaseNameEntity(
        name=Name('John'),
        count_of_requests=CountOfRequests(1),
        probability=Probability(0.85),
    )
    entity3 = BaseNameEntity(
        name=Name('Jane'),
        count_of_requests=CountOfRequests(1),
        probability=Probability(0.85),
    )

    # Test hash
    assert hash(entity1) == hash(entity1)  # Same object
    assert hash(entity1) != hash(entity2)  # Different objects with same data
    assert hash(entity1) != hash(entity3)  # Different objects with different data

    # Test equality
    assert entity1 == entity1  # Same object
