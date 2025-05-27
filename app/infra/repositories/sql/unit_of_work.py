from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self, override

from sqlalchemy.ext.asyncio import AsyncSession

from infra.repositories.sql.session_generator import SessionGenerator


@dataclass
class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def session(self) -> AsyncSession: ...

    @abstractmethod
    async def __aenter__(self) -> Self: ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    @abstractmethod
    async def save(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...


@dataclass
class UnitOfWork(IUnitOfWork):
    session_generator: SessionGenerator
    _session: AsyncSession | None = None

    @property
    @override
    def session(self) -> AsyncSession:
        if not self._session:
            raise RuntimeError('Session not initialized. Use async context manager.')
        return self._session

    @override
    async def __aenter__(self) -> Self:
        self._session = await self.session_generator.get_session().__anext__()
        return self

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        await self.close()

    @override
    async def save(self) -> None:
        """Save all changes to the database."""
        await self.session.commit()

    @override
    async def rollback(self) -> None:
        """Rollback all changes."""
        await self.session.rollback()

    @override
    async def close(self) -> None:
        """Close the database session."""
        if self._session:
            await self._session.close()
            self._session = None
