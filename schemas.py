from datetime import date as date_
from datetime import datetime
from pydantic import BaseModel


class CreateData(BaseModel):
    date: date_


class Createuser(BaseModel):
    DedeUserID: str
    SESSDATA: str
    bili_jct: str
    email: str


class ReadData(CreateData):
    id: int
    user_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class Readuser(Createuser):
    id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True