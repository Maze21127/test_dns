from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from settings import ASYNC_DATABASE_URL

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    future=True,
    echo=False,
    execution_options={"isolation_level": "AUTOCOMMIT"}
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = async_session()
    try:
        yield session
    finally:
        await session.close()
