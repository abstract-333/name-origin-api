from collections.abc import AsyncGenerator
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


@dataclass
class SessionGenerator:
    def __init__(self, db_url: str, debug: bool):
        self._engine = create_async_engine(
            url=db_url, echo=debug, pool_size=20, max_overflow=0, future=True
        )
        self._session_maker = async_sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_maker() as session:
            yield session
