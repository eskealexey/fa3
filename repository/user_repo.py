from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from backend.db import get_db
from models.transistor_mod import UserOrm
from schemas import UpdateUser


async def update_user_db(db: Annotated[Session, Depends(get_db)], update_user: UpdateUser, userid):
    stmt = (
        update(UserOrm).
            where(UserOrm.id == userid).
            values(update_user.dict(exclude_unset=True))
    )
    result = db.execute(stmt)
    db.commit()
    # logging.info(result.first())
    return result
