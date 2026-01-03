from pydantic import BaseModel

class User(BaseModel):
    _id: str
    username: str