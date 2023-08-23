import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection

from app.database.models import Base
from app.database.session import Database
from app.main import app
from settings import DATABASE_URL, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine_test = create_async_engine(
    DATABASE_URL_TEST,
    future=True,
    echo=False,
    execution_options={"isolation_level": "AUTOCOMMIT"}
)
async_session = async_sessionmaker(engine_test, expire_on_commit=False)
Base.metadata.bind = engine_test


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    app.state.db = Database(DATABASE_URL)
    await app.state.db.connect()
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
    await app.state.db.disconnect()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield conn
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def add_cities(ac: AsyncClient):
    with open('sample.txt', 'rb') as file:
        data = file.read()
    response = await ac.post('/api/cities/fromFile', files={'file': ('sample.txt', data)})
    assert response.status_code == 201


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    #loop = asyncio.get_event_loop()
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


