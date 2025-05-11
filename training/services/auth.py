from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Mapping, Any
import httpx
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/api/user/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Mapping[str, Any]:
    return await auth_service.verify_token(token)

class AuthService:
    def __init__(self):
        self.user_service_url = settings.USER_SERVICE_URL

    async def verify_token(self, token: str) -> Mapping[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                auth_header = f"Bearer {token}" if not token.startswith("Bearer ") else token
                
                response = await client.post(
                    f"{self.user_service_url}/v1/api/user/me",
                    headers={"Authorization": auth_header}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token"
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Authentication failed: {str(e)}"
                )

auth_service = AuthService() 