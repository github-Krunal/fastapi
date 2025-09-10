from pydantic import BaseModel
from typing import Optional
class FieldDefination(BaseModel):
    formControlName: str
    displayName: str
    fieldType: str
    _id: str
    lookupRepositoryName:Optional[str] = ""
    lookupField1:Optional[str] = ""
    lookupfield2:Optional[str] = ""
    
    