from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.router.user import router as userrouter
from app.router.transistor import router as transistorrouter

# from app.backend.db import create_tables, delete_tables
#
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Load the ML model
#     await delete_tables()
#     print("База очищена")
#     await create_tables()
#     print("База готова к работе")
#     yield
#     print("Выключение")
#
# app = FastAPI(lifespan=lifespan)
app = FastAPI()


@app.get("/")
async def home():
    return {'message': 'Hello, World!!!'}


app.include_router(userrouter)
app.include_router(transistorrouter)
