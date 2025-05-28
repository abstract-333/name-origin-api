from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infra.repositories.sql.base import BaseCountryRepository, BaseNameRepository
from infra.repositories.sql.country import CountrySQLAlchemyRepository
from infra.repositories.sql.name import NameSQLAlchemyRepository


@dataclass
class IUnitOfWork(ABC):
    country: BaseCountryRepository
    name: BaseNameRepository

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


@dataclass(kw_only=True)
class UnitOfWork(IUnitOfWork):
    session_factory: async_sessionmaker[AsyncSession]
    _session: AsyncSession | None = None
    country: BaseCountryRepository | None = None
    name: BaseNameRepository | None = None

    async def __aenter__(self) -> None:
        self._session = self.session_factory()

        self.country = CountrySQLAlchemyRepository(session=self._session)
        self.name = NameSQLAlchemyRepository(session=self._session)

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
