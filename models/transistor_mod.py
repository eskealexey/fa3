from backend.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class TransistorOrm(Base):
    __tablename__ = "transistors"
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    markname = Column(String, nullable=True)
    type_ = Column(Integer, ForeignKey('type_.id'))
    korpus = Column(Integer, ForeignKey('korpus.id'))
    descr = Column(String, nullable=True)
    amount = Column(Integer, default=0)
    path_file = Column(String, nullable=True)
    userid = Column(Integer, ForeignKey('users.id'))

    users = relationship('UserOrm', back_populates='userid')
    types = relationship("TypeOrm", back_populates='transistors')
    korpuss = relationship("KorpusOrm", back_populates='transistors')

class TypeOrm(Base):
    __tablename__ = "type_"

    id = Column(Integer, primary_key=True)
    type_name = Column(String)

    transistors = relationship("TransistorOrm", back_populates="types")


class KorpusOrm(Base):
    __tablename__ = "korpus"

    id = Column(Integer, primary_key=True)
    korpus_name = Column(String)

    transistors = relationship("TransistorOrm", back_populates="korpuss")



class UserOrm(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Integer, default=0)

    userid = relationship('TransistorOrm', back_populates='users')


#
# from sqlalchemy.schema import CreateTable
# print(CreateTable(TransistorOrm.__table__))
# print(CreateTable(TypeOrm.__table__))
# print(CreateTable(KorpusOrm.__table__))
# print(CreateTable(UserOrm.__table__))