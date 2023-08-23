from httpx import AsyncClient


async def from_a_to_a(city: str, ac: AsyncClient):
    response = await ac.get(
        f'/api/cities/{city}/findShortestPath', params={'to': city}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data['result']['distance'] == 0
    assert json_data['city'] == city
    assert json_data['result']['targetCity'] == city


async def from_a_to_b(from_city: str, to_city: str, target: int,ac: AsyncClient):
    response = await ac.get(
        f'/api/cities/{from_city}/findShortestPath', params={'to': to_city}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data['result']['distance'] == target
    assert json_data['city'] == from_city
    assert json_data['result']['targetCity'] == to_city


async def test_equals(ac: AsyncClient, add_cities):
    await from_a_to_a('Renton', ac)
    await from_a_to_a('SoDo', ac)
    await from_a_to_a('Factoria', ac)
    await from_a_to_a('Issaquah', ac)
    await from_a_to_a('Seattle', ac)
    await from_a_to_a('Bellevue', ac)
    await from_a_to_a('Redmond', ac)
    await from_a_to_a('Northup', ac)
    await from_a_to_a('Eastlake', ac)


async def test_non_existent_city_from(ac: AsyncClient):
    response = await ac.get(
        f'/api/cities/test/findShortestPath', params={'to': 'Northup'}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'City from not found'


async def test_non_existent_city_to(ac: AsyncClient):
    response = await ac.get(
        f'/api/cities/Northup/findShortestPath', params={'to': 'test'}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'City to not found'


async def test_find_shortest_path_correct(ac: AsyncClient):
    await from_a_to_b("Renton", "Northup", 11, ac)
    await from_a_to_b("Renton", "Seattle", 13, ac)
    await from_a_to_b("Renton", "Bellevue", 10, ac)
    await from_a_to_b("Issaquah", "Eastlake", 21, ac)
    await from_a_to_b("Redmond", "Factoria", 8, ac)
    await from_a_to_b("Bellevue", "Issaquah", 12, ac)
    await from_a_to_b("Eastlake", "SoDo", 3, ac)
    await from_a_to_b("SoDo", "Redmond", 16, ac)

