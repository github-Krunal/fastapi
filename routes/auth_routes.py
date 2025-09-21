from fastapi import APIRouter
from model.registration import Registration
from controller.auth_controller import register_user
router = APIRouter(prefix="/api", tags=["Authentication"])

@router.post("/registration")
async def register(registration: Registration):
    return register_user(registration)