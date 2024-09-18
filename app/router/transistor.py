from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from starlette import status
from typing_extensions import Annotated

from app.backend.db import get_db
from app.models.transistor_mod import TransistorOrm, TypeOrm, KorpusOrm
from app.repository.transistor_repo import update_transistor_db
from app.schemas.transistors_shem import CreateType, CreateKorpus, CreateTransistor, UpdateTransistor

router = APIRouter(
    prefix="/transistors",
    tags=["transistors"]
)


# ==========================full list transistos============================
@router.get("/fulllist")
async def get_all(db: Annotated[Session, Depends(get_db)]):
    query = select(TransistorOrm)
    result = db.execute(query)
    transistors = result.scalars().all()
    return transistors


# ==========================Create transistos============================
@router.post("/create")
async def add_transistor(db: Annotated[Session, Depends(get_db)], create_transistor: CreateTransistor):
    db.execute(insert(TransistorOrm).values(
        name=create_transistor.name,
        markname=create_transistor.markname,
        type_=create_transistor.type_,
        korpus=create_transistor.korpus,
        descr=create_transistor.descr,
        amount=create_transistor.amount,
        path_file=create_transistor.path_file
        # userid: int

    ))
    db.commit()
    return {
        'status_kod': status.HTTP_201_CREATED,
        'type_': 'Successful',
    }


# ==========================Update transistor===========================
@router.put("/update/{trid}")
async def update_user(
        db: Annotated[Session, Depends(get_db)], update_transistor: UpdateTransistor, trid: int
):
    transistor = await update_transistor_db(db=db, update_transistor=update_transistor, trid=trid)
    if transistor is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка обновления данных"
        )
    return transistor


# ===========================full list types============================
@router.get("/typelist")
async def get_type_all(db: Annotated[Session, Depends(get_db)]):
    query = select(TypeOrm)
    result = db.execute(query)
    types = result.scalars().all()
    return types


# ===========================create types============================
@router.post("/createtype")
async def add_type(db: Annotated[Session, Depends(get_db)], create_type: CreateType):
    db.execute(insert(TypeOrm).values(
        type_name=create_type.type_name,
    ))
    db.commit()
    return {
        'status_kod': status.HTTP_201_CREATED,
        'type_': 'Successful',
    }


# ===========================full list korpus============================
@router.get("/korpuslist")
async def get_korpus_all(db: Annotated[Session, Depends(get_db)]):
    query = select(KorpusOrm)
    result = db.execute(query)
    korpus = result.scalars().all()
    return korpus


# ===========================create korpus============================
@router.post("/createkorpus")
async def add_korpus(db: Annotated[Session, Depends(get_db)], create_korpus: CreateKorpus):
    db.execute(insert(KorpusOrm).values(
        korpus_name=create_korpus.korpus,
    ))
    db.commit()
    return {
        'status_kod': status.HTTP_201_CREATED,
        'korpus': 'Successful',
    }
