import logging

from fastapi import Depends
from sqlalchemy import select, column
from typing import Any, Dict, Optional, Union
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app.backend.db import get_db
from app.models.transistor_mod import UserOrm, TransistorOrm
from app.schemas.transistors_shem import UpdateTransistor
from app.schemas.users_shem import CreateUser, UpdateUser


async def update_transistor_db(db: Annotated[Session, Depends(get_db)], update_transistor: UpdateTransistor, trid):
    stmt = (
        update(TransistorOrm).
            where(TransistorOrm.id == trid).
            values(update_transistor.dict(exclude_unset=True))
    )
    result = db.execute(stmt)
    db.commit()
    # logging.info(result.first())
    return result
