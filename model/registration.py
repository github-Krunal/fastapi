# Pydantic model for request validation
from model.fieldDefination import FieldDefination
from typing import List,Optional,Any
from pydantic import BaseModel

class userCollectionRegistration(BaseModel):
    name:Optional[str]
    email: str
    username: str
    password: str
    role:Optional[str]
    status:Optional[str]
    created_at:str
    updated_at:str