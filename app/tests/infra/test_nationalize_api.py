import pytest
from app.domain.entities.name import NameStrEntity
from app.infra.repositories.nationalize_api import NationalizeRepository


@pytest.mark.asyncio
async def test_get_name_probability_success() -> None:
    repo = NationalizeRepository()
    results = await repo.get_name_probability('mark')

    assert isinstance(results, set)
    assert len(results) > 0
    assert all(isinstance(entity, NameStrEntity) for entity in results)

    # Verify probabilities are within valid range (0.0 to 1.0)
    for entity in results:
        assert 0.0 <= entity.probability.value <= 1.0
        assert entity.name.as_generic_type() == 'mark'
        assert entity.count_of_requests.value > 0


@pytest.mark.asyncio
async def test_get_name_probability_not_found() -> None:
    repo = NationalizeRepository()
    assert not await repo.get_name_probability(
        'Taumatawhakatangihangakoauauotamateaturipukakapikimaungahoronukupokai'
    )
