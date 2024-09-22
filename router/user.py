from fastapi import APIRouter, Depends, status, HTTPException, Request, Form
from sqlalchemy import insert, select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from typing_extensions import Annotated

from backend.db import get_db
from models.transistor_mod import UserOrm
# from app.main import templates
# from app.main import templates
from repository.user_repo import update_user_db
from schemas import UpdateUser

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

templates = Jinja2Templates(directory="templates")


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
        # response: Response,
        db: Annotated[Session, Depends(get_db)],
        username=Form(),
        pass1=Form(),
):
    query = select(UserOrm).where(UserOrm.username == username)
    result = db.execute(query)
    users = result.scalars().all()
    if len(users) > 0:
        for user in users:
            user_dict = vars(user)
        userid = user_dict['id']
        u_name = user_dict['username']
        password = user_dict['password']
        status = user_dict['status']
        if password == pass1:
            response = templates.TemplateResponse("main.html", {"request": request, "title": "Главная"})
            response.set_cookie(key="user_id", value=userid, expires=None, path="/")
            response.set_cookie(key="user_name", value=u_name, expires=None, path="/")
            return response
            # return {'id': userid, "username": u_name, "pass": password, 'status': status}
        else:
            return {'message': 'Неверный пароль'}


    else:
        return {'message': 'Такого пользователя нет в базе'}


@router.get('/logout')
async def logout(request: Request):
    response = templates.TemplateResponse("main.html", {"request": request, "title": "Главная"})
    response.delete_cookie(key="user_id")
    response.delete_cookie(key="user_name")
    return response