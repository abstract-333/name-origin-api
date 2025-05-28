from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from domain.entities.name import NameEntity
from infra.converters.name import NameConverter
from infra.models.name import NameOriginModel
from infra.repositories.sql.base import BaseNameRepository


@dataclass
class NameSQLAlchemyRepository(BaseNameRepository):
    session: AsyncSession

    async def get_name_origins(self, name: str) -> list[NameEntity] | None:
        query = (
            select(NameOriginModel)
            .options(joinedload(NameOriginModel.country))
            .where(NameOriginModel.name == name)
        )
        result = await self.session.execute(query)
        results = result.unique().scalars().all()
        return (
            [NameConverter().to_entity(model) for model in results] if results else None
        )

    async def get_frequent_names_by_country(self, country_name: str) -> list[NameEntity] | None:
        """Get top 5 most frequent names for a specific country.

        Args:
            country_name (str): The country name to fetch frequent names for.

        Returns:
            list[NameEntity] | None: List of top 5 name entities if found, None otherwise.
        """
        query = (
            select(NameOriginModel)
            .options(joinedload(NameOriginModel.country))
            .where(NameOriginModel.country_code == country_name)
            .order_by(desc(NameOriginModel.probability))
            .limit(5)
        )
        result = await self.session.execute(query)
        results = result.unique().scalars().all()
        return (
            [NameConverter().to_entity(model) for model in results] if results else None
        )

    async def add_name_origin(self, name_origin: NameEntity) -> None:
        name_model = NameConverter().to_model(name_origin)
        self.session.add(name_model)
        await self.session.flush()
