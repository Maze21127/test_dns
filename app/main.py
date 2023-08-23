from fastapi import FastAPI, APIRouter

from app import routes
from app.database.session import Database

from settings import DATABASE_URL


async def on_startup():
    app.state.db = Database(DATABASE_URL)
    await app.state.db.connect()


async def on_shutdown():
    await app.state.db.disconnect()


app = FastAPI(title="FSP Service")
app.add_event_handler('startup', on_startup)
app.add_event_handler('shutdown', on_shutdown)
main_api_router = APIRouter(prefix='/api')
main_api_router.include_router(routes.cities.router, tags=['Города'])
main_api_router.include_router(routes.edges.router, tags=['Пути'])
app.include_router(main_api_router)

