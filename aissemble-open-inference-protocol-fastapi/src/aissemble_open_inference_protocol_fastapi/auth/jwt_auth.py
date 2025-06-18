###
# #%L
# aiSSEMBLE::Open Inference Protocol::FastAPI
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from fastapi import HTTPException, status
from ..config.oip_config import OIPConfig
import jwt

config = OIPConfig()


def verify_jwt_token(authorization):
    """
    This method checks for the existence of a Bearer token and extracts the payload (user/subject, etc...)
    :param authorization: The FastAPI HTTPAuthorizationCredentials (scheme and credentials)
    :return: the unencrypted jwt payload
    """
    if authorization is None:
        # No Authorization header means this is an anonymous user
        payload = {"sub": "Anonymous", "name": "Anonymous"}
    else:
        if not authorization.scheme == "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing Authorization header",
            )
        try:
            secret_key = config.auth_secret()
            algorithm = config.auth_algorithm()
            payload = jwt.decode(
                authorization.credentials, secret_key, algorithms=[algorithm]
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    return payload


def authenticate_and_authorize(authz_adapter, authorization, action, resource):
    """
    This method verifies the jwt is valid and then calls the authz adapter to see if the
    user can perform the requested action on the resource.
    :param authz_adapter: The adapter that communicates with the Authz backend
    :param authorization: The HTTPAuthorizationCredentials object extracted from the Authorization Header
    :return: if the user/subject is not-authorized then a 403 error is raised.
    """
    token_data = verify_jwt_token(authorization)
    if not authz_adapter.authorize(
        user=token_data.get("sub"), action=action, resource=resource
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
