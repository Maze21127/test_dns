from fastapi import APIRouter, HTTPException, UploadFile, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.session import get_db
from app.schemas import CityCreate, ShortestPathOut, ShortestPathResult, CityOut
from app.service.cities import create_city, get_all_cities, load_cities_from_file, delete_cities
from app.service.find_distance import get_shortest_path

router = APIRouter(prefix='/cities')


@router.post("/", response_model=CityOut)
async def create(city: CityCreate, db: AsyncSession = Depends(get_db)) -> CityOut:
    new_city = await create_city(city, db)
    if new_city:
        return new_city
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something went wrong")


@router.get('/', response_model=list[CityOut])
async def get_all(db: AsyncSession = Depends(get_db)) -> list[CityOut]:
    data = await get_all_cities(db)
    return data


@router.get('/{city}/findShortestPath',
            response_model=ShortestPathOut)
async def get_all(city: str, to: str = Query(), db: AsyncSession = Depends(get_db)) -> ShortestPathOut:
    distance = await get_shortest_path(db, city, to)
    return ShortestPathOut(
        city=city,
        result=ShortestPathResult(distance=distance, targetCity=to)
    )


@router.post('/fromFile', response_model=list[CityOut], status_code=201)
async def load_cities(file: UploadFile, db: AsyncSession = Depends(get_db)) -> list[CityOut]:
    file_data: bytes = await file.read()
    await load_cities_from_file(file_data, db)
    data: list[CityOut] = await get_all_cities(db)
    return data


@router.delete('/', status_code=204)
async def delete_all_cities(db: AsyncSession = Depends(get_db)) -> None:
    await delete_cities(db)
