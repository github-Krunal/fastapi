# Pydantic model for request validation
from model.fieldDefination import FieldDefination
from typing import List,Optional,Any
from pydantic import BaseModel

class SaveFrameworkObject(BaseModel):
    repositoryID:Optional[str] = None
    record: Any
    recordID: Optional[str] = None