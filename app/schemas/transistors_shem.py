from pydantic import BaseModel

class CreateTransistors(BaseModel):
    name: str
    markname: str
    type_: int
    korpus: int
    descr: str
    amount: int
    path_file: str
    userid: int


class CreateType(BaseModel):
    type_: str


class CreateKorpus(BaseModel):
    korpus: str