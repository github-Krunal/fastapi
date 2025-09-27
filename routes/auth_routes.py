from fastapi import APIRouter
from model.login import Login
from model.registration import Registration
from controller.auth_controller import register_user,user_login
from constant.api_constant import API_PREFIX,USER_REGISTRATION,USER_LOGIN
router = APIRouter(prefix=API_PREFIX, tags=["Authentication"])

@router.post(USER_REGISTRATION)
async def register(registration: Registration):
    return register_user(registration)

@router.post(USER_LOGIN)
async def login(Login: Login):
    return user_login(Login)
