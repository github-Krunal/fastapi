# Pydantic model for request validation
from pydantic import BaseModel
class RepositoyDefination(BaseModel):
    RepositoryName: str
    Description: str
    CreatedDate: str