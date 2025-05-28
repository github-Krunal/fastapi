# Pydantic model for request validation
from pydantic import BaseModel
class OfferBanner(BaseModel):
    ImageURL: str
    OfferName: str
    RouteURL: str