from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from domain.entities.country import CountryEntity
from infra.converters.country import CountryConverter
from infra.models.country import CountryModel
from infra.repositories.sql.base import BaseCountryRepository


@dataclass
class CountrySQLAlchemyRepository(BaseCountryRepository):
    session: AsyncSession

    async def get_country(self, name: str) -> CountryEntity | None:
        query = select(CountryModel).where(CountryModel.iso_alpha2_code == name)
        result = await self.session.execute(query)
        result_scalar = result.scalar_one_or_none()
        return CountryConverter().to_entity(result_scalar) if result_scalar else None

    async def add_country(self, country: CountryEntity) -> CountryEntity:
        country_model = CountryConverter().to_model(country)
        self.session.add(country_model)
        await self.session.flush()
        return country

    async def delete_country(self, name: str) -> None:
        query = delete(CountryModel).where(CountryModel.iso_alpha2_code == name)
        await self.session.execute(query)

    async def update_country(
        self, name: str, country: CountryEntity
    ) -> CountryEntity | None:
        query = (
            update(CountryModel)
            .where(CountryModel.iso_alpha2_code == name)
            .values(**country.__dict__)
            .returning(CountryModel)
        )
        result = await self.session.execute(query)
        result_scalar = result.scalar_one_or_none()
        return CountryConverter().to_entity(result_scalar) if result_scalar else None
