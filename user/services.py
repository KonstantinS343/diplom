from jose import jwt, JWTError
from typing import Mapping, Any

from config import oauth2_scheme, keycloak_openid, keycloak_admin, auth_settings
from fastapi import Depends, HTTPException, status


class AuthService:
    @classmethod
    async def verify_token(cls, token: str) -> Mapping[str, Any]:
        try:
            public_key = keycloak_openid.public_key()
            payload = jwt.decode(
                token,
                "-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----",
                algorithms=["RS256"],
                options={"verify_aud": False},
            )

            return payload
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)) -> Mapping[str, Any]:
        payload = await cls.verify_token(token)
        return {
            "email": payload.get("email"),
            "username": payload.get("preferred_username"),
            "sub": payload.get("sub")
        }

    @classmethod
    async def login(self, email: str, password: str) -> Mapping[str, Any]:
        try:
            token = keycloak_openid.token(
                username=email, password=password, grant_type="password"
            )
            user_info = keycloak_openid.userinfo(token["access_token"])
            print(token)

            return {
                "id": user_info.get("sub"),
                "access_token": token["access_token"],
                "refresh_token": token["refresh_token"],
                "expires_in": token["expires_in"],
                "refresh_expires_in": token["refresh_expires_in"],
                "token_type": "Bearer",
                "user": {
                    "email": user_info.get("email"),
                    "username": user_info.get("preferred_username"),
                }
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
    async def me(csl, token: str) -> Mapping[str, Any]:
        try:
            user_info = keycloak_openid.userinfo(token)
            return {
                "username": user_info.get("preferred_username"),
                "email": user_info.get("email"),
                "sub": user_info.get("sub")
            }
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to fetch profile: {str(e)}"
        )
