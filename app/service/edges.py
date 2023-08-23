from app.database.session import Database
from app.schemas import EdgeCreate


async def create_edge(edge: EdgeCreate, db: Database):
    stmt = f"INSERT INTO public.edge (from_city_id, to_city_id, distance) " \
           f"VALUES ({edge.from_city_id}, {edge.to_city_id}, {edge.distance})"
    await db.execute(stmt)


async def delete_edges(db: Database) -> None:
    await db.execute("DELETE FROM public.edge")