from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Edge
from app.schemas import EdgeCreate


class EdgeDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def fetch_all(self):
        query = select(Edge)
        result = await self.db_session.execute(query)
        return result.scalars()

    async def drop(self):
        query = delete(Edge)
        await self.db_session.execute(query)

    async def create(self, body: EdgeCreate) -> Edge:
        edge = Edge(
            from_city_id=body.from_city_id,
            to_city_id=body.to_city_id,
            distance=body.distance
        )
        self.db_session.add(edge)
        await self.db_session.flush()
        return edge
