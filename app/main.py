from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.router.transistor import router as trans_router
from app.router.user import router as userrouter

app = FastAPI()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "title": "Главная"})


app.include_router(userrouter)
app.include_router(trans_router)

templates = Jinja2Templates(directory="app/templates")
app.mount('/static', StaticFiles(directory="app/public"))

