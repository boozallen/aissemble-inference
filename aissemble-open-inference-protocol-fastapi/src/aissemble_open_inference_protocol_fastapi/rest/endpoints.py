###
# #%L
# aiSSEMBLE::Open Inference Protocol::FastAPI
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPBearer
from aissemble_open_inference_protocol_fastapi.handlers.default_handler import (
    DefaultHandler,
)
from aissemble_open_inference_protocol_fastapi.auth.default_adapter import (
    DefaultAdapter,
)
from aissemble_open_inference_protocol_fastapi.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelMetadataErrorResponse,
    ModelReadyResponse,
    ServerReadyResponse,
    ServerLiveResponse,
    ServerMetadataResponse,
    ServerMetadataErrorResponse,
)
from aissemble_open_inference_protocol_fastapi.auth.jwt_auth import (
    authenticate_and_authorize,
)

security = HTTPBearer(auto_error=False)
AUTH_ACTION_READ = "read"
AUTH_RESOURCE_DATA = "data"

router = APIRouter(
    prefix="/v2",
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/models/{model_name}/infer",
    summary="Perform a given models inference",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=InferenceResponse,
)
def infer_model(
    model_name,
    payload: InferenceRequest,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    authorization: str = Depends(security),
) -> InferenceResponse:
    """
    Perform inference using the specified model and return the prediction results.
    """
    authenticate_and_authorize(
        authz_adapter, authorization, AUTH_ACTION_READ, AUTH_RESOURCE_DATA
    )

    return handler.infer(model_name=model_name, payload=payload)


@router.post(
    "/models/{model_name}/versions/{model_version}/infer",
    summary="Perform a given models inference given a specific version",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=InferenceResponse,
)
async def infer_model_version(
    model_name,
    model_version,
    payload: InferenceRequest,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    authorization: str = Depends(security),
) -> InferenceResponse:
    """
    Perform inference using the specified model version and return the prediction results.
    """
    authenticate_and_authorize(
        authz_adapter, authorization, AUTH_ACTION_READ, AUTH_RESOURCE_DATA
    )

    return handler.infer(
        model_name=model_name, model_version=model_version, payload=payload
    )


@router.get(
    "/models/{model_name}",
    summary="Get model metadata",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=ModelMetadataResponse,
    responses={
        400: {
            "model": ModelMetadataErrorResponse,
            "description": "Returned if the model metadata request is invalid or fails.",
        },
        404: {
            "model": ModelMetadataErrorResponse,
            "description": "Returned if the model or model version is not found.",
        },
    },
)
def model_metadata(
    model_name: str,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    authorization: str = Depends(security),
) -> ModelMetadataResponse:
    """
    Retrieve metadata for the specified model.
    """
    authenticate_and_authorize(
        authz_adapter, authorization, AUTH_ACTION_READ, AUTH_RESOURCE_DATA
    )

    return handler.model_metadata(model_name=model_name)


@router.get(
    "/models/{model_name}/versions/{model_version}",
    summary="Get model metadata for a specific version",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=ModelMetadataResponse,
    responses={
        400: {
            "model": ModelMetadataErrorResponse,
            "description": "Returned if the model metadata request is invalid or fails.",
        },
        404: {
            "model": ModelMetadataErrorResponse,
            "description": "Returned if the model or model version is not found.",
        },
    },
)
def model_version_metadata(
    model_name: str,
    model_version: str,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    authorization: str = Depends(security),
) -> ModelMetadataResponse:
    """
    Retrieve metadata for the specified model version.
    """
    authenticate_and_authorize(
        authz_adapter, authorization, AUTH_ACTION_READ, AUTH_RESOURCE_DATA
    )

    return handler.model_metadata(model_name=model_name, model_version=model_version)


@router.get(
    "/models/{model_name}/ready",
    summary="Check if model is ready",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=ModelReadyResponse,
)
def model_ready(
    model_name: str,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    authorization: str = Depends(security),
) -> ModelReadyResponse:
    """
    Check if the specified model is ready to serve requests.
    """
    authenticate_and_authorize(
        authz_adapter, authorization, AUTH_ACTION_READ, AUTH_RESOURCE_DATA
    )

    return handler.model_ready(model_name=model_name)


@router.get(
    "/models/{model_name}/versions/{model_version}/ready",
    summary="Check if specific model version is ready",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=ModelReadyResponse,
)
def model_version_ready(
    model_name: str,
    model_version: str,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    authorization: str = Depends(security),
) -> ModelReadyResponse:
    """
    Check if the specified model version is ready to serve requests.
    """
    authenticate_and_authorize(
        authz_adapter, authorization, AUTH_ACTION_READ, AUTH_RESOURCE_DATA
    )

    return handler.model_ready(model_name=model_name, model_version=model_version)


@router.get(
    "/health/ready",
    summary="Check if server is ready",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=ServerReadyResponse,
)
def server_ready(
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    authorization: str = Depends(security),
) -> ServerReadyResponse:
    """
    Check if the server returns the readiness probe.
    """
    authenticate_and_authorize(
        authz_adapter, authorization, AUTH_ACTION_READ, AUTH_RESOURCE_DATA
    )

    return handler.server_ready()


@router.get(
    "/health/live",
    summary="Check if server is live",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=ServerLiveResponse,
)
def server_live(
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    authorization: str = Depends(security),
) -> ServerLiveResponse:
    """
    Check if the server returns the liveness probe.
    """
    authenticate_and_authorize(
        authz_adapter, authorization, AUTH_ACTION_READ, AUTH_RESOURCE_DATA
    )

    return handler.server_live()


@router.get(
    "",
    summary="Get server metadata",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=ServerMetadataResponse,
    responses={
        400: {
            "model": ServerMetadataErrorResponse,
            "description": "Returned if the server metadata request is invalid or fails.",
        },
    },
)
def server_metadata(
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    authorization: str = Depends(security),
) -> ServerMetadataResponse:
    """
    Retrieve metadata for the server
    """
    authenticate_and_authorize(
        authz_adapter, authorization, AUTH_ACTION_READ, AUTH_RESOURCE_DATA
    )

    return handler.server_metadata()
