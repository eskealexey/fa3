from fastapi import FastAPI, Request, Cookie

from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
from typing_extensions import Annotated
from fastapi.staticfiles import StaticFiles
from router.transistor import router as trans_router
from router.user import router as userrouter
from router.media import router as mediarouter

app = FastAPI()


@app.get("/")
async def home(request: Request, user_name: Annotated[str, Cookie()] = None):
    print(user_name)
    return templates.TemplateResponse("main.html", {"request": request, "title": "Главная", "user_name": user_name})


app.include_router(userrouter)
app.include_router(trans_router)
app.include_router(mediarouter)

templates = Jinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory="public"))
