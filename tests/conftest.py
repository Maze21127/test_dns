import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database.models import Base
from app.database.session import get_db
from app.main import app
from settings import DATABASE_TEST_URL

engine_test = create_async_engine(
    DATABASE_TEST_URL,
    future=True,
    echo=False,
    execution_options={"isolation_level": "AUTOCOMMIT"}
)
async_session = async_sessionmaker(engine_test, expire_on_commit=False)
Base.metadata.bind = engine_test


async def get_test_db() -> AsyncSession:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_db] = get_test_db


@pytest_asyncio.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


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
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


