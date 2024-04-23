from typing import Annotated, List, Optional
from typing_extensions import Doc

from urllib.parse import urlencode

import httpx

from jose import jwt, jwk


class BaseOauth2:
    def __init__(
        self,
        client_id: Annotated[str, Doc("")],
        client_secret: Annotated[str, Doc("")],
        authorize_endpoint: Annotated[str, Doc("")],
        access_token_endpoint: Annotated[str, Doc("")],
        refresh_token_endpoint: Annotated[Optional[str], Doc("")] = None,
        revoke_token_endpoint: Annotated[Optional[str], Doc("")] = None,
        base_scopes: Annotated[Optional[List[str]], Doc("")] = None,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_endpoint = authorize_endpoint
        self.access_token_endpoint = access_token_endpoint
        self.refresh_token_endpoint = refresh_token_endpoint
        self.revoke_token_endpoint = revoke_token_endpoint
        self.base_scopes = base_scopes

    def get_authorization_url(
        self,
        redirect_url: Annotated[str, Doc("")],
        scopes: Annotated[Optional[List[str]], Doc("")] = None,
        **kwargs,
    ):
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_url": redirect_url,
        }

        scopes = scopes or self.base_scopes
        if scopes:
            params["scope"] = " ".join(scopes)

        params.update(**kwargs)

        return f"{self.authorize_endpoint}?{urlencode(params)}"

    async def authorization_code_callback(
        self,
        code: Annotated[
            str, Doc("Authorization code received from authorization server")
        ],
        redirect_uri: Annotated[str, Doc("")],
        code_verifier: Annotated[str, Doc("")],
    ):
        data = dict(
            grant_type="authorization_code",
            code=code,
            redirect_uri=redirect_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(self.access_token_endpoint, data=data)
            return response.json()


class OpenID(BaseOauth2):
    def __init__(
        self,
        client_id: Annotated[str, Doc("")],
        client_secret: Annotated[str, Doc("")],
        openid_configuration_endpoint: Annotated[str, Doc("")],
        base_scopes: Annotated[Optional[List[str]], Doc("")] = None,
    ) -> None:
        with httpx.Client() as client:
            response = client.get(openid_configuration_endpoint)
            self.openid_configuration = response.json()

        authorize_endpoint = self.openid_configuration.get("authorization_endpoint")
        access_token_endpoint = self.openid_configuration.get("token_endpoint")
        refresh_token_supported = "refresh_token" in self.openid_configuration.get(
            "grant_types_supported", []
        )

        refresh_token_endpoint = (
            access_token_endpoint if refresh_token_supported else None
        )

        revoke_token_endpoint = self.openid_configuration.get("revocation_endpoint")

        base_scopes = base_scopes or ["openid", "profile", "offline_access"]

        with httpx.Client() as client:
            response = client.get(self.openid_configuration.get("jwks_uri"))
            keys = response.json()
            self.keys = [jwk.construct(key) for key in keys["keys"]]

        super().__init__(
            client_id,
            client_secret,
            authorize_endpoint,
            access_token_endpoint,
            refresh_token_endpoint,
            revoke_token_endpoint,
            base_scopes,
        )

    def decode_token(self, token: str):
        return jwt.decode(token, key=self.keys, audience="account")

    def authorize_client(self):
        """
        Authorize client by its id and secret using client_credentials grant type
        """
        params = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type="client_credentials",
        )

        with httpx.Client() as client:
            response = client.post(self.access_token_endpoint, data=params)
            return response.json()

    def __repr__(self) -> str:
        return f"{self.keys}, {self.authorize_endpoint}"


kc = OpenID(
    client_id="admin-cli",
    client_secret="Lednrb2CsYzYvRm3D2BfMOAT5MUPRut9",
    openid_configuration_endpoint="https://auth.cekocloud.com/realms/industry-dev/.well-known/openid-configuration",
)

print(kc)

data = kc.authorize_client()
print(data)

print(kc.decode_token(data["access_token"]))
