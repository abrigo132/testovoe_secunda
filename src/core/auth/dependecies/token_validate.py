from fastapi import status, HTTPException, Header

from core import settings


def verify_auth_api_token(
    api_token: str = Header(..., alias="X-Auth-API-Token")
) -> None:

    if api_token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid API token"
        )

    if api_token != settings.security.api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token"
        )
