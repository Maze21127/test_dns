import heapq

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from app.database.dals.city import CityDAL
from app.database.dals.edge import EdgeDAL
from app.schemas import CityOut


async def _get_city_by_name(name: str, session: AsyncSession) -> CityOut | None:
    city_dal = CityDAL(session)
    city = await city_dal.get_city_by_name(name)
    return CityOut(id=city.id, name=city.name) if city is not None else None


async def get_shortest_path(session: AsyncSession, from_city: str, to_city: str):
    async with session.begin():
        if not await _get_city_by_name(from_city, session):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City from not found")
        if not await _get_city_by_name(to_city, session):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City to not found")
        graph = await _load_graph(session)
    result = dijkstra(graph, from_city, to_city)
    return result


async def _load_graph(session: AsyncSession):
    city_dal = CityDAL(session)
    edge_dal = EdgeDAL(session)
    cities = await city_dal.fetch_all()
    edges = await edge_dal.fetch_all()
    graph = {}
    for city in cities:
        graph[city.name] = {'name': city.name, 'edges': {}}

    for edge in edges:
        graph[edge.from_city.name]['edges'][edge.to_city.name] = edge.distance

    return graph


def dijkstra(graph, start, end):
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
