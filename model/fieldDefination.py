from pydantic import BaseModel
class FieldDefination(BaseModel):
    formControlName: str
    label: str
    fieldType: str
    