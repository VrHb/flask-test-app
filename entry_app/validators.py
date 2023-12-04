from datetime import datetime
from pydantic import BaseModel, ValidationError


class User(BaseModel):
    name: str | None = None
    email: str
    password: str

class EntrySerializer(BaseModel):
    id: int
    text: str
    date: datetime
    user_id: int

    class Config:
        from_attributes = True
