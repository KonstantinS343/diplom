from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID, KeycloakAdmin


class AuthConfig(BaseSettings):
    url: str
    realm_name: str
    client_id: str
    client_secret: str
    admin_user: str
    admin_password: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", env_prefix="KEYCLOAK_"
    )


auth_settings = AuthConfig()

keycloak_openid = KeycloakOpenID(
    server_url=auth_settings.url,
    client_id=auth_settings.client_id,
    realm_name=auth_settings.realm_name,
    client_secret_key=auth_settings.client_secret,
)

keycloak_admin = KeycloakAdmin(
    server_url=auth_settings.url,
    username=auth_settings.admin_user,
    password=auth_settings.admin_password,
    realm_name=auth_settings.realm_name,
    verify=True
)


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{auth_settings.url}/realms/{auth_settings.realm_name}/protocol/openid-connect/auth",
    tokenUrl=f"{auth_settings.url}/realms/{auth_settings.realm_name}/protocol/openid-connect/token",
    auto_error=False,
)
