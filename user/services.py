from jose import jwt, JWTError
from typing import Mapping, Any

from config import oauth2_scheme, keycloak_openid, keycloak_admin, auth_settings
from fastapi import Depends, HTTPException, status


class AuthService:
    @classmethod
    async def get_current_user(csl, token: str = Depends(oauth2_scheme)) -> Mapping[str, Any]:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            public_key = keycloak_openid.public_key()
            payload = jwt.decode(
                token,
                "-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----",
                algorithms=["RS256"],
                audience=auth_settings.client_id,
            )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @classmethod
    async def login(self, username: str, password: str) -> Mapping[str, Any]:
        try:
            token = keycloak_openid.token(
                username=username, password=password, grant_type="password"
            )
            return {
                "access_token": token["access_token"],
                "refresh_token": token["refresh_token"],
                "expires_in": token["expires_in"],
                "refresh_expires_in": token["refresh_expires_in"],
                "token_type": "Bearer",
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Login failed: {str(e)}"
            )
            
    @classmethod
    async def register(
        csl,
        username: str,
        password: str,
        email: str
    ) -> Mapping[str, Any]:
        try:
            user = keycloak_admin.create_user(
                {
                    "username": username,
                    "email": email,
                    "enabled": True,
                    "credentials": [{"type": "password", "value": password, "temporary": False}],
                }, exist_ok=False
            )
            return {"message": "User registered successfully", "user_id": user}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Registration failed: {str(e)}"
            )
            
    @classmethod
    async def logout(csl, token) -> Mapping[str, Any]:
        try:
            keycloak_openid.logout(token)
            return {"message": "Logged out successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Logout failed: {str(e)}"
            )
            
    @classmethod
    async def me(csl, current_user: Mapping[str, Any] = Depends(get_current_user)) -> Mapping[str, Any]:
        try:
            user_info = keycloak_openid.userinfo(current_user["sub"])
            return {
                "username": user_info.get("preferred_username"),
                "email": user_info.get("email"),
                "sub": user_info.get("sub")
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to fetch profile: {str(e)}"
        )
