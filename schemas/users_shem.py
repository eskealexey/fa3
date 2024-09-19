from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    password: str
    status: int

class UpdateUser(BaseModel):
    password: str
    status: int
