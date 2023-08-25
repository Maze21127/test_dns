from fastapi import FastAPI, APIRouter

from app import routes


app = FastAPI(title="FSP Service")
main_api_router = APIRouter(prefix='/api')
main_api_router.include_router(routes.cities.router, tags=['Города'])
main_api_router.include_router(routes.edges.router, tags=['Пути'])
app.include_router(main_api_router)

