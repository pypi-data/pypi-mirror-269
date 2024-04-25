import base64

from constance import config as _config
from rest_framework.test import APIClient as _APIClient
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as _TokenObtainPairSerializer,
)

__all__ = [
    "configure_api_client",
]


def configure_api_client(  # noqa
    client: _APIClient,
    set_header_version=True,
    basic_auth=False,
    access_token=None,
    user=None,
    password=None,
):
    headers = {}
    if set_header_version:
        version = _config.ALLOWED_VERSIONS.split(" ")[0]
        headers["HTTP_ACCEPT"] = f"application/json; version={version}"

    if access_token is not None and not basic_auth:
        headers["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"

    if user is not None and not basic_auth:
        access = str(_TokenObtainPairSerializer.get_token(user).access_token)
        headers["HTTP_AUTHORIZATION"] = f"Bearer {access}"
        client.force_authenticate(user=user)

    if basic_auth and password:
        access = base64.b64encode(str.encode(f"{user.email}:{password}")).decode(
            "iso-8859-1",
        )
        headers["HTTP_AUTHORIZATION"] = f"Basic {access}"

    client.credentials(**headers)
