from fastapi import APIRouter
from model.registration import Registration
from controller.auth_controller import register_user
from constant.api_constant import API_PREFIX,USER_REGISTRATION
router = APIRouter(prefix=API_PREFIX, tags=["Authentication"])

@router.post(USER_REGISTRATION)
async def register(registration: Registration):
    return register_user(registration)
