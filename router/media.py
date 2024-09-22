# import shutil
#
# from fastapi import APIRouter, Depends, Request, Response
# from fastapi import File, UploadFile
# from sqlalchemy import select
# from sqlalchemy.orm import Session
# from starlette.templating import Jinja2Templates
# from typing_extensions import Annotated
# from backend.db import get_db
# from main import *
# from models.transistor_mod import TransistorOrm
#
# router = APIRouter(
#     prefix="/media",
#     tags=["media"]
# )
# templates = Jinja2Templates(directory="templates")
#

# =============================загрузить Даташит=======================================
# @router.post("/{trid}")
# async def datasheet(
#         response: Response,
#         request: Request,
#         trid: int,
#         db: Annotated[Session, Depends(get_db)],
#         upload_file: UploadFile = File(),
# ):
#     print(trid)
#     global path
#     try:
#         upload_file.filename = upload_file.filename.lower()
#
#         # path = f'public/media/{upload_file.filename}'
#         path = MEDIA_ROOT + '/' + upload_file.file
#         print(path)
#         query = select(TransistorOrm).where(TransistorOrm.id == trid)
#         result = db.execute(query)
#         transistor = result.scalars().one()
#         transistor.path_file = path
#         db.commit()
#         db.refresh(transistor)
#         with open(path, 'wb+') as buffer:
#             shutil.copyfileobj(upload_file.file, buffer)
#
#         return {
#             "response": response,
#             "trid": trid,
#             "request": request,
#             "file": upload_file,
#             "filename": path,
#             "type": upload_file.content_type,
#         }
#     except Exception as e:
#         print(e)
#         return {
#             "trid": trid,
#             # "request": request,
#             "file": upload_file,
#             # "filename": path,
#             "type": upload_file.content_type,
#         }
