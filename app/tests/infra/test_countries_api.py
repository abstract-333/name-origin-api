import pytest
import httpx
from domain.entities.country import CountryEntity
from infra.repositories.countries_api import CountriesAPIRepository


@pytest.mark.asyncio
async def test_get_country_success() -> None:
    repo = CountriesAPIRepository()
    result = await repo.get_country('US')

    assert isinstance(result, CountryEntity)
    assert result.iso_alpha2_code == 'US'
    assert result.common_name == 'United States'
    assert result.official_name == 'United States of America'
    assert result.region == 'Americas'
    assert result.sub_region == 'North America'
    assert result.independent is True
    assert result.capital == {'Washington, D.C.'}
    assert result.capital_lat
    assert result.capital_long
    assert result.flag_png
    assert result.flag_svg
    assert result.flag_alt
    assert result.coat_of_arms_png
    assert result.coat_of_arms_svg
    assert result.borders == {'CAN', 'MEX'}


@pytest.mark.asyncio
async def test_get_country_not_found() -> None:
    repo = CountriesAPIRepository()
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await repo.get_country('NONEXISTENT')
    assert exc_info.value.response.status_code == 400


@pytest.mark.asyncio
async def test_get_list_of_countries() -> None:
    repo = CountriesAPIRepository()
    results = await repo.get_list_of_countries()

    assert isinstance(results, set)
    assert len(results) > 0
    assert all(isinstance(country, CountryEntity) for country in results)

    # Verify we can find some common countries
    country_codes = {country.iso_alpha2_code for country in results}
    assert 'US' in country_codes
    assert 'GB' in country_codes
    assert 'FR' in country_codes
