from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class UserOrm(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Integer, default=0)
