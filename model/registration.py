# Pydantic model for request validation
from model.fieldDefination import FieldDefination
from typing import List,Optional,Any
from pydantic import BaseModel

class Registration(BaseModel):
    name:Optional[str]= None
    email: str
    username: str
    password: str
    role:Optional[str]= None
    status:Optional[str]= None
    created_at:Optional[str]= None
    updated_at:Optional[str]= None