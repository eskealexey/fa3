from fastapi import FastAPI, Request, Cookie, Response

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing_extensions import Annotated

from app.router.transistor import router as trans_router
from app.router.user import router as userrouter

app = FastAPI()


@app.get("/")
async def home(request: Request, user_name : Annotated[str, Cookie()] = None):
    print(user_name)
    return templates.TemplateResponse("main.html", {"request": request, "title": "Главная", "user_name": user_name})


app.include_router(userrouter)
app.include_router(trans_router)

templates = Jinja2Templates(directory="app/templates")
app.mount('/static', StaticFiles(directory="app/public"))
