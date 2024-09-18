from fastapi import APIRouter, Depends, status, HTTPException, Request, Form, Body
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from typing_extensions import Annotated
from app.backend.db import get_db

from sqlalchemy import insert, select, update, delete

# from app.main import templates
# from app.main import templates
from app.repository.user_repo import update_user_db
from app.models.transistor_mod import UserOrm
from app.schemas.users_shem import CreateUser, UpdateUser

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

templates = Jinja2Templates(directory="app/templates")


# ==============================Список пользователей ============================
@router.get("/all_users")
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    query = select(UserOrm)
    result = db.execute(query)
    users = result.scalars().all()
    return users


# ==================================Создание пользователя==========================
@router.post("/create")
async def create_user(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        username=Form(...),
        pass1=Form(...),
        pass2=Form(...)
):
    if pass1 == pass2:
        try:
            db.execute(insert(UserOrm).values(
                username=username,
                password=pass1,
                status=0
            ))
            db.commit()
        except IntegrityError as e:
            print(e)
            return templates.TemplateResponse(
                "registration.html",
                {"request": request, "title": "Регистрация", 'message': 'Такой пользователь зарегистрирован'}
            )
    else:
        return templates.TemplateResponse("registration.html", {"request": request, "title": "Регистрация"})

    return templates.TemplateResponse("registration_ok.html",
                                      {"request": request,
                                       "title": "Регистрация",
                                       "message": f"Пользователь {username} зарегистрирован"
                                       })


# =====================================Обновление пользователя=====================
@router.put("/update/{userid}")
async def update_user(
        db: Annotated[Session, Depends(get_db)], update_user: UpdateUser, userid: int
):
    user = await update_user_db(db=db, update_user=update_user, userid=userid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка обновления данных"
        )
    return user


@router.delete("/delete")
async def delete_users(db: Annotated[Session, Depends(get_db)]):
    db.execute(delete(UserOrm))
    db.commit()
    return {'message': 'Delete All'}


#
@router.get("/registr")
async def registr(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request, "title": "Регистрация"})


@router.get('/login')
async def logw(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Авторизация"})


@router.post("/login")
async def log_in(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        username=Form(...),
        pass1=Form(...),
):
    try:
        query = select(UserOrm).where(UserOrm.username == username)
        result = db.execute(query)
        user = result.scalars().all()
        if UserOrm(user).password == pass1:
            print("URA")
        else:
            print('DIRA')
    except:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    return {'request': request, "username": user, "pass": pass1}
