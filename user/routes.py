from fastapi import APIRouter, Depends, Header, HTTPException, status
from typing import Mapping, Any, Optional

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
async def profile(
    authorization: Optional[str] = Header(None),
    service: AuthService = Depends()
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    token = authorization.split(" ")[1]
    current_user = await service.verify_token(token)
    return await service.me(token)
