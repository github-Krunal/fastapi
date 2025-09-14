from pydantic import BaseModel
from typing import Optional,List
class FieldDefination(BaseModel):
    formControlName: str
    displayName: str
    fieldType: str
    _id: str
    lookupRepositoryName:Optional[str] = ""
    lookupField1:Optional[str] = ""
    lookupField2:Optional[str] = ""
    options: Optional[List[str]] = []
    
    