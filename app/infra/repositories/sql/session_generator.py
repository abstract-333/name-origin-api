from dataclasses import dataclass

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)


@dataclass
class AsyncSessionFactory:
    _async_engine = None
    _async_session_maker = None
    url: str
    debug: bool

    def _create_instance(self) -> async_sessionmaker[AsyncSession]:
        self._async_engine: AsyncEngine = create_async_engine(
            url=self.url, echo=self.debug, pool_size=20, max_overflow=0
        )
        self._async_session_maker = async_sessionmaker(
            self._async_engine, expire_on_commit=False
        )
        return self._async_session_maker

    def get_async_session_maker(self) -> async_sessionmaker[AsyncSession]:
        self._create_instance()
        return self._async_session_maker
