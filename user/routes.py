from fastapi import APIRouter, Depends
from typing import Mapping, Any

from services import AuthService
from schemas import LoginRequest, RegisterRequest, LogoutRequest


router = APIRouter(tags=["user"], prefix="/v1/api/user")


@router.post("/login")
async def login(request: LoginRequest, service: AuthService = Depends()):
    return await service.login(
        email=request.email,
        password=request.password,
    )


@router.post("/register")
async def register(request: RegisterRequest, service: AuthService = Depends()):
    print(request.username)
    return await service.register(
        username=request.username,
        password=request.password,
        email=request.email,
    )


@router.post("/logout")
async def logout(request: LogoutRequest, service: AuthService = Depends()):
    return await service.logout(request.refresh_token)


@router.post("/me")
async def profile(current_user: Mapping[str, Any] = Depends(AuthService.get_current_user), service: AuthService = Depends()):
    return await service.me(current_user)
