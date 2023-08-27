import heapq
from typing import Iterable

from asyncpg import UniqueViolationError, ForeignKeyViolationError
from fastapi import HTTPException
from starlette import status

from app.database.session import Database
from app.schemas import CityCreate, CityOut, DatabaseStatuses, EdgeCreate
from app.service.edges import create_edge


async def _load_cities(cities: Iterable[str], db: Database) -> dict[str, int]:
    result = dict()
    for city in cities:
        new_city = await create_city(CityCreate(name=city), db)
        result[new_city.name] = new_city.id
    return result


async def delete_cities(db: Database) -> None:
    try:
        await db.execute("DELETE FROM public.city")
    except ForeignKeyViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Need to delete edges first")


async def load_cities_from_file(data: bytes, db: Database) -> None:
    rows = data.decode().split('\n')
    cities = await _load_cities(set(
        row.split()[0] for row in rows
    ), db)
    for row in rows:
        edge_data = row.split()
        edge = EdgeCreate(
            from_city_id=cities[edge_data[0]],
            to_city_id=cities[edge_data[1]],
            distance=edge_data[2]
        )
        await create_edge(edge, db)


async def create_city(city: CityCreate, db: Database) -> CityOut:
    stmt = f"INSERT INTO public.city (name) VALUES ('{city.name}')"
    try:
        result = await db.execute(stmt)
        city_in_db = await db.fetch(f"SELECT id FROM public.city WHERE name = '{city.name}'")
        if result == DatabaseStatuses.INSERT_OK.value:
            return CityOut(name=city.name, id=city_in_db[0]['id'])
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="City already exists")


async def get_all_cities(db: Database) -> list[CityOut]:
    stmt = "SELECT * FROM public.city"
    result = await db.fetch(stmt)
    return [CityOut(name=row['name'], id=row['id']) for row in result]


async def get_city_id(db: Database, city_name: str) -> bool:
    stmt = f"SELECT * from public.city WHERE name = '{city_name}'"
    result = await db.fetch(stmt)
    return result[0]['id'] if result else None


async def get_shortest_path(db: Database, from_city: int, to_city: int) -> int:
    graph = await _load_graph(db)
    result = dijkstra(graph, from_city, to_city)
    return result


async def _load_graph(db: Database) -> dict:
    cities = await db.fetch("SELECT * FROM public.city")
    edges = await db.fetch("SELECT * FROM public.edge")

    graph = {}
    for city in cities:
        graph[city['id']] = {'name': city['name'], 'edges': {}}

    for edge in edges:
        graph[edge['from_city_id']]['edges'][edge['to_city_id']] = edge['distance']

    return graph


def dijkstra(graph, start, end) -> int:
    distances = {city_id: float('inf') for city_id in graph}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        current_distance, current_city = heapq.heappop(heap)
        if current_distance > distances[current_city]:
            continue

        for neighbor, weight in graph[current_city]['edges'].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))

    return distances[end]
