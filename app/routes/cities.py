from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.params import Query
from starlette import status
from starlette.requests import Request

from app.schemas import CityCreate, ShortestPathOut, ShortestPathResult, CityOut
from app.service.cities import create_city, get_all_cities, get_shortest_path, get_city_id, load_cities_from_file, \
    delete_cities

router = APIRouter(prefix='/cities')


@router.post("/", response_model=CityOut)
async def create(request: Request, city: CityCreate) -> CityOut:
    new_city = await create_city(city, request.app.state.db)
    if new_city:
        return new_city
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something went wrong")


@router.get('/', response_model=list[CityOut])
async def get_all(request: Request) -> list[CityOut]:
    data = await get_all_cities(request.app.state.db)
    return data


@router.get('/{city}/findShortestPath',
            response_model=ShortestPathOut)
async def get_all(request: Request, city: str, to: str = Query()) -> ShortestPathOut:
    db = request.app.state.db
    city_from_id = await get_city_id(db, city)
    if not city_from_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City from not found")
    city_to_id = await get_city_id(db, to)
    if not city_to_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City to not found")
    distance = await get_shortest_path(db, city_from_id, city_to_id)
    return ShortestPathOut(
        city=city,
        result=ShortestPathResult(distance=distance, targetCity=to)
    )


@router.post('/fromFile', response_model=list[CityOut], status_code=201)
async def load_cities(request: Request, file: UploadFile) -> list[CityOut]:
    file_data: bytes = await file.read()
    await load_cities_from_file(file_data, request.app.state.db)
    data: list[CityOut] = await get_all_cities(request.app.state.db)
    return data


@router.delete('/', status_code=204)
async def delete_all_cities(request: Request) -> None:
    await delete_cities(request.app.state.db)
