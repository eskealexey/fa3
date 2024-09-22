import shutil

from fastapi import APIRouter, Depends, HTTPException, Request, Form, Cookie, Response

from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from typing_extensions import Annotated
from backend.db import get_db
from fastapi import File, UploadFile, Form
from main import *
# from main import MEDIA_ROOT
from models.transistor_mod import TransistorOrm, TypeOrm, KorpusOrm
from repository.transistor_repo import update_transistor_db
from schemas.transistors_shem import CreateType, CreateKorpus, UpdateTransistor

router = APIRouter(
    prefix="/transistors",
    tags=["transistors"]
)
templates = Jinja2Templates(directory="templates")


# ==========================full list transistos============================
@router.get("/")
async def get_all(request: Request, db: Annotated[Session, Depends(get_db)], user_id=Cookie(default=None), user_name=Cookie(),):
    if user_id != None:
        query = select(TransistorOrm).where(TransistorOrm.userid == user_id)
        result = db.execute(query)
        transistors = result.scalars().all()

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


#========================форма редактировани транзистора=================
@router.get("/edit/{trid}")
async def edit_transistor(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        trid: int,
        user_id = Cookie()
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
        q_type = select(TypeOrm)
        r_type = db.execute(q_type)
        types = r_type.scalars().all()

        q_korpus = select(KorpusOrm)
        r_korpus = db.execute(q_korpus)
        korpus = r_korpus.scalars().all()
        return templates.TemplateResponse(
            "transistor_edit.html",
            {
                "request": request,
                "title": "Транзистор",
                "transistor": transistor,
                "types": types,
                "korpus": korpus,
                "user_id": user_id,
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
# @router.put("/update/{trid}")
# async def update_transistr(
#         db: Annotated[Session, Depends(get_db)], update_transistor: UpdateTransistor, trid=int
# ):
#     transistor = await update_transistor_db(db=db, update_transistor=update_transistor, trid=trid)
#     if transistor is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Ошибка обновления данных"
#         )
#     return transistor

@router.post("/edit")
async def update_transistr(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        # update_transistor: UpdateTransistor,
        trid=int,
        name = Form(),
        markname = Form(),
        type_ = Form(),
        korpus = Form(),
        descr = Form()
):
    if request.method == 'POST':
        query = update(TransistorOrm).values(
             name=name,
             markname=markname,
             type_=type_,
             korpus=korpus,
             descr=descr
         ).where(TransistorOrm.id == trid)
        db.execute(query)
        db.commit()
        return templates.TemplateResponse("transistor_id.html",
                                          {"request": request, "title": "Транзисторы",
                                           "trid": trid}, )


    return templates.TemplateResponse("transistor_id.html",
                                          {"request": request, "title": "Транзисторы",
                                           "trid": trid}, )

    #     {
    #     'request': 'request',
    # }


# =====================Добавить количество деталей =====================
@router.post("/{trid}")
async def add_amount(
        request: Request,
        db: Annotated[Session, Depends(get_db)],
        trid: int,
        act=Form(default=None),
        quantity=Form(default=0),
):
    query = select(TransistorOrm).where(TransistorOrm.id == trid)
    result = db.execute(query)
    transistor = result.scalars().one()
    total = int(transistor.amount)
    if act is not None:
        if act == 'add':
            total += int(quantity)
        elif (act == 'del') and (total >= int(quantity)):
            total -= int(quantity)
        else:
            error = 'удаляется больше чем есть'

        if transistor == None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})

        transistor.amount = total
        db.commit()  # сохраняем изменения
        db.refresh(transistor)

        return templates.TemplateResponse("transistor_id.html",
                                          {"request": request, "title": "Транзисторы", "transistor": transistor,
                                           "trid": trid}, )

    else:
        error = 'не выбрано действие'
    return  templates.TemplateResponse("transistor_id.html",
                                          {"request": request, "title": "Транзисторы", "transistor": transistor,
                                           "trid": trid},)

#=======================================================================================
@router.post("/{trid}")
async def datasheet(
        response: Response,
        request: Request,
        trid: int,
        db: Annotated[Session, Depends(get_db)],
        upload_file: UploadFile = File(),
):
    global path
    print(trid)
    # global path
    try:
        upload_file.filename = upload_file.filename.lower()

        # path = f'public/media/{upload_file.filename}'
        path = MEDIA_ROOT + '/' + upload_file.file
        print(path)
        query = select(TransistorOrm).where(TransistorOrm.id == trid)
        result = db.execute(query)
        transistor = result.scalars().one()
        transistor.path_file = path
        db.commit()
        db.refresh(transistor)
        with open(path, 'wb+') as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        return {
            "response": response,
            "trid": trid,
            "request": request,
            "file": upload_file,
            "filename": path,
            "type": upload_file.content_type,
        }
    except Exception as e:
        print(e)
        return {
            "trid": trid,
            # "request": request,
            "file": upload_file,
            "filename": path,
            "type": upload_file.content_type,
        }



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


@router.get('/find/')
async def find(
        request: Request,
        response: Response,
        db: Annotated[Session, Depends(get_db)],
        find = Form(),
        userid = Cookie('user_id')
):
    if request.method == 'GET':
        query = select(TransistorOrm).filter_by(userid == TransistorOrm.userid, TransistorOrm.name.__contains__(find))
        result = db.execute(query)
        transistors = result.scalars().all()
        return templates.TemplateResponse("transistor.html",
                                          {"request": request, "title": "Транзисторы", "transistors": transistors})