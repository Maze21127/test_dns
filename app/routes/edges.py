from fastapi import APIRouter
from starlette import status
from starlette.requests import Request

from app.schemas import EdgeCreate
from app.service.edges import create_edge, delete_edges

router = APIRouter(prefix='/edges')


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EdgeCreate)
async def create(request: Request, edge: EdgeCreate) -> EdgeCreate:
    await create_edge(edge, request.app.state.db)
    return edge


@router.delete('/', status_code=204)
async def delete_all_edges(request: Request) -> None:
    await delete_edges(request.app.state.db)
