from model.registration  import Registration
from database import userRegistrationCollection

def register_user(registration: Registration):
    result = userRegistrationCollection.insert_one(registration.dict())
    return {"id": str(result.inserted_id), "message": "User registered"}