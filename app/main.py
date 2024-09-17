from fastapi import FastAPI

from app.router.user import router as userrouter

app = FastAPI()


@app.get("/")
async def home():
    return {'message': 'Hello, World!!!'}


app.include_router(userrouter)