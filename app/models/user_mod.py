# from app.backend.db import Base
# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# # from app.models.transistor_mod import TransistorOrm
#
#
# class UserOrm(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     status = Column(Integer, default=0)
#
#     transistor = relationship('TransistorOrm', back_populates='users')



# from sqlalchemy.schema import CreateTable
# print(CreateTable(UserOrm.__table__))
