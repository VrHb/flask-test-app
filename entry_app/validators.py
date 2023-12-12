from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str | None = None
    email: EmailStr
    password: str

class EntrySerializer(BaseModel):
    id: int
    text: str
    date: datetime
    user_id: int

    class Config:
        from_attributes = True

class EntryText(BaseModel):
    text: str
