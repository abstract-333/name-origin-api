from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from httpx import Response
from typing import Any


@pytest.mark.asyncio
async def test_get_name_origins_missing_parameter(
    app: FastAPI,
    client: TestClient,
) -> None:
    """Test getting name origins without name parameter."""
    url = app.url_path_for('get_name_origins_handler')
    response: Response = client.get(url=url, params={'name': ''})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_data = response.json()
    assert json_data['detail']['error'] == 'Name parameter is required'


@pytest.mark.asyncio
async def test_get_name_origins_nonexistent_name(
    app: FastAPI,
    client: TestClient,
) -> None:
    """Test getting name origins for a non-existent name."""
    url = app.url_path_for('get_name_origins_handler')
    response: Response = client.get(
        url=url, params={'name': 'flasdfasdjfhadsfljkhadsfadsfa'}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_data = response.json()
    assert (
        json_data['detail']['error'] == "Name 'flasdfasdjfhadsfljkhadsfadsfa' not found"
    )


@pytest.mark.asyncio
async def test_get_name_origins_success(
    app: FastAPI,
    client: TestClient,
) -> None:
    """Test getting name origins successfully."""

    url = app.url_path_for('get_name_origins_handler')
    response: Response = client.get(url=url, params={'name': 'John'})

    assert response.status_code == status.HTTP_200_OK
    json_data: list[dict[str, Any]] = response.json()
    assert isinstance(json_data, list)
    # Verify the structure of returned data
    if json_data:  # If we got any results
        first_result = json_data[0]
        assert 'name' in first_result
        assert 'country' in first_result
        assert 'probability' in first_result


@pytest.mark.asyncio
async def test_get_popular_names_missing_parameter(
    app: FastAPI,
    client: TestClient,
) -> None:
    """Test getting popular names without country parameter."""
    url = app.url_path_for('get_popular_names_by_country_handler')
    response: Response = client.get(url=url, params={'country': ''})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_data = response.json()
    assert json_data['detail']['error'] == 'Country parameter is required'


@pytest.mark.asyncio
async def test_get_popular_names_nonexistent_country(
    app: FastAPI,
    client: TestClient,
) -> None:
    """Test getting popular names for a non-existent country."""
    url = app.url_path_for('get_popular_names_by_country_handler')
    response: Response = client.get(url=url, params={'country': 'zz'})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_data = response.json()
    assert json_data['detail']['error'] == 'No names found for country zz'


@pytest.mark.asyncio
async def test_get_popular_names_success(
    app: FastAPI,
    client: TestClient,
) -> None:
    """Test getting popular names successfully."""

    url = app.url_path_for('get_popular_names_by_country_handler')
    response: Response = client.get(url=url, params={'country': 'US'})

    assert response.status_code == status.HTTP_200_OK
    json_data: list[dict[str, Any]] = response.json()
    assert isinstance(json_data, list)
    # Verify we get at most 5 results as per the handler's documentation
    assert len(json_data) <= 5
