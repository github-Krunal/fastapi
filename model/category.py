# Pydantic model for request validation
from pydantic import BaseModel
class Category(BaseModel):
    Name: str
    Type:str