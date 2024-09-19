from fastapi import APIRouter, Depends, HTTPException, Request, Form, Cookie
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates
from typing_extensions import Annotated

from app.backend.db import get_db
from app.models.transistor_mod import TransistorOrm, TypeOrm, KorpusOrm
from app.repository.transistor_repo import update_transistor_db
from app.schemas.transistors_shem import CreateType, CreateKorpus, CreateTransistor, UpdateTransistor

router = APIRouter(
    prefix="/transistors",
    tags=["transistors"]
)
templates = Jinja2Templates(directory="app/templates")


# ==========================full list transistos============================
@router.get("/")
async def get_all(request: Request, db: Annotated[Session, Depends(get_db)], user_id=Cookie(default=None)):
    if user_id != None:
        query = select(TransistorOrm).where(TransistorOrm.userid == user_id)
        result = db.execute(query)
        transistors = result.scalars().all()
        if len(transistors) > 0:
            return templates.TemplateResponse("transistor.html",
                                              {"request": request, "title": "Транзисторы", "transistors": transistors})
    else:
        return {'massage': "Необходимо авторизоваться"}


# ==========================страница с формой для добавления транзистора============================
@router.get("/create")
async def form_add_transistor(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        user_id=Cookie(),
        user_name=Cookie(),

):
    q_type_ = select(TypeOrm)
    r_type = db.execute(q_type_)
    types = r_type.scalars().all()

    q_korpus = select(KorpusOrm)
    r_korpus = db.execute(q_korpus)
    korpus = r_korpus.scalars().all()

    return templates.TemplateResponse(
        "transistor_forma_add.html",
        {"request": request,
         "title": "Добавление транзистора",
         "types": types,
         "korpus": korpus,
         "user_id": user_id,
         "user_name": user_name, }
    )


# ==========================вывод транзистора============================
@router.get("/{trid}")
async def get_transistor(
        request: Request,
        trid: int,
        db: Annotated[Session, Depends(get_db)],
):
    query = select(TransistorOrm).where(TransistorOrm.id == trid)
    result = db.execute(query)
    transistor = result.scalars().one()
    if transistor is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка обновления данных"
        )
    else:
        q_type = select(TypeOrm.type_name).where(TypeOrm.id == transistor.type_)
        r_type = db.execute(q_type)
        types = r_type.scalars().one()

        q_korpus = select(KorpusOrm.korpus_name).where(KorpusOrm.id == transistor.korpus)
        r_korpus = db.execute(q_korpus)
        korpus = r_korpus.scalars().one()

        return templates.TemplateResponse(
            "transistor_id.html",
            {
                "request": request,
                "title": "Транзистор",
                "transistor": transistor,
                "types": types,
                "korpus": korpus,
            })


# ==========================Create transistos============================
@router.post("/add_tr")
async def add_transistor(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        name=Form(title="name"),
        markname=Form(),
        type_=Form(),
        korpus=Form(),
        descr=Form(),
        # path_file = Form(),
        user_id=Form(),
):
    user_name = Cookie()
    try:
        db.execute(insert(TransistorOrm).values(
            name=name,
            markname=markname,
            type_=type_,
            korpus=korpus,
            descr=descr,
            amount=0,
            path_file='',
            userid=user_id,
        ))
        db.commit()
        query = select(TransistorOrm).where(TransistorOrm.userid == user_id)
        result = db.execute(query)
        transistors = result.scalars().all()

        return templates.TemplateResponse("transistor.html",
                                          {"request": request, "title": "Транзисторы", "transistors": transistors,
                                           "user_id": user_id})
    except HTTPException as e:
        print(e)
        return templates.TemplateResponse(
            "transistor_forma_add.html",
            {"request": request, "title": "Добавление транзистора", 'message': 'Такой пользователь зарегистрирован'}
        )


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


# =====================Добавть количество деталей =====================
@router.post("/{trid}")
async def add_amount(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        trid: int,
        act=Form(default=None),
        quantity=Form(default=0),
):
    query = select(TransistorOrm.amount).where(TransistorOrm.id == trid)
    result = db.execute(query)
    total = int(result.scalars().one())

    if act is not None:
        if act == 'add':
            total += int(quantity)
        elif (act == 'del') and (total >= quantity):
            total -= int(quantity)
        else:
            error = 'удаляется больше чем есть'



    else:
        error = 'не выбрано действие'


    # if (request.POST):
    #     error = ''
    #     data_dict = request.POST.dict()
    #     act = data_dict.get('act')
    #     quantity = data_dict.get('quantity ')
    #     try:
    #         quantity = abs(int(quantity))
    #         total = data.amount
    #         print(total)
    #         if act is not None:
    #             if act == 'add':
    #                 total += quantity
    #             elif (act == 'del') and (total >= quantity):
    #                 total -= quantity
    #             else:
    #                 error = 'удаляется больше чем есть'
    #
    #             data.amount = total
    #             data.save(update_fields=['amount'])
    #         else:
    #             error = 'не выбрано действие'
    #
    #         context = {
    #             'title': 'Транзистор',
    #             'data': data,
    #             'error': error,
    #         }
    #     except Exception as err:
    #         print(err)
    #         error = 'не число'
    #         context = {
    #             'title': 'Транзистор',
    #             'data': data,
    #             'error': error,
    #         }
    #     return render(request, 'app/transistor_id.html', context=context)
    # else:
    #     context = {
    #         'title': 'Транзистор',
    #         'data': data,
    #         'error': '',
    #     }
    #     return render(request, 'app/transistor_id.html', context=context)

    pass


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


@router.delete("/delete")
async def delete_users(db: Annotated[Session, Depends(get_db)]):
    db.execute(delete(TransistorOrm))
    db.commit()
    return {'message': 'Delete All'}
