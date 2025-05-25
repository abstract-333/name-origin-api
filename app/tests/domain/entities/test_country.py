from datetime import datetime, UTC

from domain.entities.country import CountryEntity


def test_country_entity_creation() -> None:
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

    assert country.iso_alpha2_code == 'US'
    assert country.common_name == 'United States'
    assert country.official_name == 'United States of America'
    assert country.region == 'Americas'
    assert country.sub_region == 'North America'
    assert country.independent is True
    assert country.capital == {'Washington, D.C.'}
    assert country.capital_lat == 38.8951
    assert country.capital_long == -77.0364
    assert country.flag_png == 'https://flagcdn.com/w320/us.png'
    assert country.flag_svg == 'https://flagcdn.com/us.svg'
    assert country.flag_alt == 'The flag of the United States of America'
    assert (
        country.coat_of_arms_png
        == 'https://mainfacts.com/media/images/coats_of_arms/us.png'
    )
    assert (
        country.coat_of_arms_svg
        == 'https://mainfacts.com/media/images/coats_of_arms/us.svg'
    )
    assert country.borders == {'CAN', 'MEX'}
    assert isinstance(country.created_at, datetime)
    assert country.created_at.tzinfo == UTC


def test_country_entity_optional_fields() -> None:
    country = CountryEntity(
        iso_alpha2_code='US',
        common_name='United States',
        official_name='United States of America',
        region='Americas',
        sub_region='North America',
        independent=None,
        capital=set(),
        capital_lat=None,
        capital_long=None,
        flag_png='https://flagcdn.com/w320/us.png',
        flag_svg='https://flagcdn.com/us.svg',
        flag_alt=None,
        coat_of_arms_png=None,
        coat_of_arms_svg=None,
        borders=set(),
    )

    assert country.independent is None
    assert country.capital == set()
    assert country.capital_lat is None
    assert country.capital_long is None
    assert country.flag_alt is None
    assert country.coat_of_arms_png is None
    assert country.coat_of_arms_svg is None
    assert country.borders == set()


def test_country_entity_capital_name() -> None:
    # Test with single capital
    country1 = CountryEntity(
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
        flag_alt=None,
        coat_of_arms_png=None,
        coat_of_arms_svg=None,
        borders=set(),
    )
    assert country1.capital_name == 'Washington, D.C.'

    # Test with multiple capitals
    country2 = CountryEntity(
        iso_alpha2_code='ZA',
        common_name='South Africa',
        official_name='Republic of South Africa',
        region='Africa',
        sub_region='Southern Africa',
        independent=True,
        capital={'Pretoria', 'Bloemfontein', 'Cape Town'},
        capital_lat=None,
        capital_long=None,
        flag_png='https://flagcdn.com/w320/za.png',
        flag_svg='https://flagcdn.com/za.svg',
        flag_alt=None,
        coat_of_arms_png=None,
        coat_of_arms_svg=None,
        borders=set(),
    )
    assert country2.capital_name == 'Bloemfontein, Cape Town, Pretoria'

    # Test with no capital
    country3 = CountryEntity(
        iso_alpha2_code='AQ',
        common_name='Antarctica',
        official_name='Antarctica',
        region='Antarctic',
        sub_region='',
        independent=None,
        capital=set(),
        capital_lat=None,
        capital_long=None,
        flag_png='https://flagcdn.com/w320/aq.png',
        flag_svg='https://flagcdn.com/aq.svg',
        flag_alt=None,
        coat_of_arms_png=None,
        coat_of_arms_svg=None,
        borders=set(),
    )
    assert country3.capital_name == ''
