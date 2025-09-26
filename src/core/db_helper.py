from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from core import settings


class DbHelper:

    def __init__(
        self, url: str, pool_size: int, max_overflow: int, echo: bool, echo_pool: bool
    ) -> None:

        self.async_engine: AsyncEngine = create_async_engine(
            url=url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo=echo,
            echo_pool=echo_pool,
        )

        self.async_session_factory: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.async_engine,
                autoflush=False,
                expire_on_commit=False,
                autocommit=False,
            )
        )

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as session:
            yield session

    async def dispose(self) -> None:
        await self.async_engine.dispose()


db_helper = DbHelper(
    url=str(settings.db.url),
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
)
