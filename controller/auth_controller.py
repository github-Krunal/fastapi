from fastapi import HTTPException
from authentication.hashing import verify_password, hash_password
from model.login import Login
from model.registration  import Registration
from database import userRegistrationCollection
from  authentication.jwt_handler import create_access_token
from  model.user import User
from fastapi.responses import JSONResponse

def register_user(registration: Registration):
    reg_dict = registration.model_dump()

    # Hash the password
    reg_dict["password"] = hash_password(reg_dict["password"])

    # Save to DB
    result = userRegistrationCollection.insert_one(reg_dict)

    return {
        "id": str(result.inserted_id),
        "message": "User registered"
    }

def user_login(login: Login):
    login_dict = login.model_dump()  # 👈 Convert to dict

    # Find the user with matching email and password
    user:User = userRegistrationCollection.find_one({
        "$or": [
            {"email": login_dict["username"]},
            {"username": login_dict["username"]}
        ],
        "password": login_dict["password"]
    })

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(login_dict['password'], user['password']):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({"user_id": str(user['_id'])})

    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "_id": str(user['_id']),
            "username": user.username
        }
    }
