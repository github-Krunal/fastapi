# Pydantic model for request validation
from model.fieldDefination import FieldDefination
from typing import List,Optional
from pydantic import BaseModel
class RepositoyDefination(BaseModel):
    repositoryName: str
    description: str
    createdDate: str
    createdBy: str
    fieldDefination:Optional[List[FieldDefination]] = None