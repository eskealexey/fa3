from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app.backend.db import get_db

from sqlalchemy import insert, select, update
from app.repository.user_repo import update_user_db
from app.models.transistor_mod import UserOrm
from app.schemas.users_shem import CreateUser, UpdateUser

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

#==============================Список пользователей ============================
@router.get("/all_users")
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    query = select(UserOrm)
    result = db.execute(query)
    users = result.scalars().all()
    return users


#==================================Создание пользователя==========================
@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(UserOrm).values(
        username=create_user.username,
        password=create_user.password,
        status=create_user.status
    ))
    db.commit()
    return {
        'status_kod': status.HTTP_201_CREATED,
        'transaction': 'Successful',
    }

#=====================================Обновление пользователя=====================
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
async def delete_user():
    pass
