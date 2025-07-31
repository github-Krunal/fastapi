from pydantic import BaseModel
class FieldDefination(BaseModel):
    formControlName: str
    displayName: str
    fieldType: str
    _id: str
    
    