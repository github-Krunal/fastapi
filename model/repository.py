# Pydantic model for request validation
from model.fieldDefination import FieldDefination
from typing import List,Optional
from pydantic import BaseModel
class RepositoyDefination(BaseModel):
    RepositoryName: str
    Description: str
    CreatedDate: str
    FieldDefination:Optional[List[FieldDefination]] = None