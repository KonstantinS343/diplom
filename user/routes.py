from fastapi import APIRouter, Depends
from typing import Mapping, Any

from services import AuthService
from schemas import LoginRequest, RegisterRequest
from config import oauth2_scheme


router = APIRouter(tags=["user"], prefix="/user")


@router.post("/login")
async def login(request: LoginRequest, service: AuthService = Depends()):
    return await service.login(
        username=request.username,
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
async def logout(refresh_token: str = Depends(oauth2_scheme), service: AuthService = Depends()):
    return await service.logout(refresh_token)


@router.post("/me")
async def profile(current_user: Mapping[str, Any] = Depends(AuthService.get_current_user), service: AuthService = Depends()):
    return await service.me(current_user)
