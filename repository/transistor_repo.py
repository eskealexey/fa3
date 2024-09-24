# from fastapi import Depends
# from sqlalchemy import update
# from sqlalchemy.orm import Session
# from typing_extensions import Annotated
#
# from backend.db import get_db
# from models.transistor_mod import TransistorOrm
# from schemas.transistors_shem import UpdateTransistor
#
#
# async def update_transistor_db(db: Annotated[Session, Depends(get_db)], update_transistor: UpdateTransistor, trid):
#     stmt = (
#         update(TransistorOrm).
#             where(TransistorOrm.id == trid).
#             values(update_transistor.model_dump_json(exclude_unset=True))
#     )
#     result = db.execute(stmt)
#     db.commit()
#     # logging.info(result.first())
#     return result
