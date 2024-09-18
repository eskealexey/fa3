from pydantic import BaseModel

class CreateTransistor(BaseModel):
    name: str
    markname: str
    type_: int
    korpus: int
    descr: str
    amount: int
    path_file: str
    # userid: int


class UpdateTransistor(BaseModel):
    name: str
    markname: str
    type_: int
    korpus: int
    descr: str
    amount: int
    path_file: str
    userid: int


class CreateType(BaseModel):
    type_name: str


class CreateKorpus(BaseModel):
    korpus: str