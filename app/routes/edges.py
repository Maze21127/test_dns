
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.service.edges import delete_edges

router = APIRouter(prefix='/edges')


@router.delete('/', status_code=204)
async def delete_all_edges(db: AsyncSession = Depends(get_db)):
    await delete_edges(db)
