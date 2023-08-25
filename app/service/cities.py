from typing import Iterable

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.dals.city import CityDAL, CityAlreadyExists
from app.schemas import CityCreate, CityOut, EdgeCreate
from app.service.edges import create_edge


async def _load_cities(cities: Iterable[str], session: AsyncSession) -> dict[str, int]:
    result = dict()
    for city in cities:
        new_city = await create_city(CityCreate(name=city), session)
        result[new_city.name] = new_city.id
    return result


async def delete_cities(session: AsyncSession) -> None:
    city_dal = CityDAL(session)
    try:
        await city_dal.drop()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Need to delete edges first")


async def load_cities_from_file(data: bytes, session: AsyncSession) -> None:
    rows = data.decode().split('\n')
    cities = await _load_cities(set(
        row.split()[0] for row in rows
    ), session)
    for row in rows:
        edge_data = row.split()
        edge = EdgeCreate(
            from_city_id=cities[edge_data[0]],
            to_city_id=cities[edge_data[1]],
            distance=edge_data[2]
        )
        await create_edge(edge, session)


async def create_city(body: CityCreate, session: AsyncSession) -> CityOut:
    async with session.begin():
        city_dal = CityDAL(session)
        try:
            city = await city_dal.create(body)
        except CityAlreadyExists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="City already exists")
        return CityOut(id=city.id, name=city.name)


async def get_all_cities(session: AsyncSession) -> list[CityOut]:
    async with session.begin():
        city_dal = CityDAL(session)
        cities = await city_dal.fetch_all()
        return [CityOut(
            id=city.id,
            name=city.name
        ) for city in cities]



