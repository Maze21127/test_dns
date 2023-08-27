from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dals.edge import EdgeDAL
from app.schemas import EdgeCreate


async def create_edge(body: EdgeCreate, session: AsyncSession) -> None:
    async with session.begin():
        edge_dal = EdgeDAL(session)
        await edge_dal.create(body)


async def delete_edges(session: AsyncSession) -> None:
    city_dal = EdgeDAL(session)
    await city_dal.drop()
