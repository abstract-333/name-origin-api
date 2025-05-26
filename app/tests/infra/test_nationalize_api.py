import pytest
from domain.entities.name import NameStrEntity
from infra.repositories.base import BaseNameOriginAPIRepository


@pytest.mark.asyncio
async def test_get_name_probability_success(
    name_origin_repository: BaseNameOriginAPIRepository,
) -> None:
    results = await name_origin_repository.get_name_origins_probability('mark')

    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(entity, NameStrEntity) for entity in results)

    # Verify probabilities are within valid range (0.0 to 1.0)
    for entity in results:
        assert 0.0 <= entity.probability.value <= 1.0
        assert entity.name.as_generic_type() == 'mark'
        assert entity.count_of_requests.value > 0


@pytest.mark.asyncio
async def test_get_name_probability_not_found(
    name_origin_repository: BaseNameOriginAPIRepository,
) -> None:
    assert not await name_origin_repository.get_name_origins_probability(
        'Taumatawhakatangihangakoauauotamateaturipukakapikimaungahoronukupokai'
    )
