# Pydantic model for request validation
from model.fieldDefination import FieldDefination
from typing import List,Optional,Any
from pydantic import BaseModel

class Registration(BaseModel):
    email: str
    username: str
    password: str