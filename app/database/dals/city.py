from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import City
from app.schemas import CityCreate


class CityAlreadyExists(Exception):
    """City already exists"""


class CityDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def _is_city_exists(self, name: str) -> bool:
        return bool(await self.get_city_by_name(name))

    async def get_city_by_name(self, name: str) -> City | None:
        normalized_username = func.lower(name)
        query = select(City).where(func.lower(City.name) == normalized_username)
        result = await self.db_session.execute(query)
        return result.scalar() if not None else None

    async def drop(self):
        query = delete(City)
        await self.db_session.execute(query)

    async def fetch_all(self):
        query = select(City)
        result = await self.db_session.execute(query)
        return result.scalars()

    async def create(self, body: CityCreate) -> City:
        if await self._is_city_exists(body.name):
            raise CityAlreadyExists()
        city = City(
            name=body.name,
        )
        self.db_session.add(city)
        await self.db_session.flush()
        return city
