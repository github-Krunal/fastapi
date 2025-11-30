from model.login import Login
from model.registration  import Registration
from database import userRegistrationCollection
from fastapi.responses import JSONResponse

def register_user(registration: Registration):
    result = userRegistrationCollection.insert_one(registration.dict())
    return {"id": str(result.inserted_id), "message": "User registered"}

def user_login(login: Login):
    login_dict = login.dict()  # 👈 Convert to dict

    # Find the user with matching email and password
    user = userRegistrationCollection.find_one({
        "$or": [
            {"email": login_dict["username"]},
            {"username": login_dict["username"]}
        ],
        "password": login_dict["password"]
    })

    if user:
        user["_id"] = str(user["_id"])
        return {"message": "Login successful", "user":user}
    else:
       return JSONResponse(
        status_code=200,
        content={"message": "Invalid email or password"}
    )