###
# #%L
# aiSSEMBLE::Open Inference Protocol::FastAPI
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from fastapi import APIRouter, status, Depends, Request
from typing import Optional, List
from fastapi.security import HTTPBearer
from aissemble_open_inference_protocol_shared.handlers.default_handler import (
    DefaultHandler,
)
from aissemble_open_inference_protocol_shared.auth.default_adapter import (
    DefaultAdapter,
)
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelMetadataErrorResponse,
    ModelReadyResponse,
    ServerReadyResponse,
    ServerLiveResponse,
    ServerMetadataResponse,
    ServerMetadataErrorResponse,
    ResponseOutput,
)
from aissemble_open_inference_protocol_shared.auth.jwt_auth import (
    authenticate_and_authorize,
)
from aissemble_open_inference_protocol_shared.auth.auth_context import (
    AuthContext,
)
from aissemble_open_inference_protocol_shared.codecs.utils import (
    decode_inference_request,
    encode_inference_response,
    encode_response_output,
    get_content_type,
)
from krausening.logging import LogManager
from functools import partial

security = HTTPBearer(auto_error=False)
AUTH_ACTION_READ = "read"
AUTH_RESOURCE_DATA = "data"

logger = LogManager.get_instance().get_logger("OIPEndpoints")

router = APIRouter(
    prefix="/v2",
    responses={404: {"description": "Not found"}},
)

# Partially initialize AuthContext with some common defaults
PartialAuthContext = partial(
    AuthContext,
    auth_action=AUTH_ACTION_READ,
    auth_resource=AUTH_RESOURCE_DATA,
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
    request: Request,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    bearer_token: str = Depends(security),
) -> InferenceResponse:
    """
    Perform inference using the specified model and return the prediction results.
    """
    auth_context = PartialAuthContext(
        authz_adapter=authz_adapter,
        bearer_token=bearer_token,
        user_ip=_get_user_ip_from_request(request),
        request_url=str(request.url),
    )

    authenticate_and_authorize(auth_context)

    raw_request_payload = payload
    decoded_payload = decode_inference_request(payload)
    result = handler.infer(model_name=model_name, payload=decoded_payload)

    return build_inference_response(
        model_name=model_name, request=raw_request_payload, result=result
    )


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
    request: Request,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    bearer_token: str = Depends(security),
) -> InferenceResponse:
    """
    Perform inference using the specified model version and return the prediction results.
    """
    auth_context = PartialAuthContext(
        authz_adapter=authz_adapter,
        bearer_token=bearer_token,
        user_ip=_get_user_ip_from_request(request),
        request_url=str(request.url),
    )

    authenticate_and_authorize(auth_context)

    raw_request_payload = payload
    decoded_payload = decode_inference_request(payload)
    result = handler.infer(model_name=model_name, payload=decoded_payload)

    return build_inference_response(
        model_name=model_name,
        request=raw_request_payload,
        result=result,
        model_version=model_version,
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
    request: Request,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    bearer_token: str = Depends(security),
) -> ModelMetadataResponse:
    """
    Retrieve metadata for the specified model.
    """
    auth_context = PartialAuthContext(
        authz_adapter=authz_adapter,
        bearer_token=bearer_token,
        user_ip=_get_user_ip_from_request(request),
        request_url=str(request.url),
    )

    authenticate_and_authorize(auth_context)

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
    request: Request,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    bearer_token: str = Depends(security),
) -> ModelMetadataResponse:
    """
    Retrieve metadata for the specified model version.
    """
    auth_context = PartialAuthContext(
        authz_adapter=authz_adapter,
        bearer_token=bearer_token,
        user_ip=_get_user_ip_from_request(request),
        request_url=str(request.url),
    )

    authenticate_and_authorize(auth_context)

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
    request: Request,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    bearer_token: str = Depends(security),
) -> ModelReadyResponse:
    """
    Check if the specified model is ready to serve requests.
    """
    auth_context = PartialAuthContext(
        authz_adapter=authz_adapter,
        bearer_token=bearer_token,
        user_ip=_get_user_ip_from_request(request),
        request_url=str(request.url),
    )

    authenticate_and_authorize(auth_context)

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
    request: Request,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    bearer_token: str = Depends(security),
) -> ModelReadyResponse:
    """
    Check if the specified model version is ready to serve requests.
    """
    auth_context = PartialAuthContext(
        authz_adapter=authz_adapter,
        bearer_token=bearer_token,
        user_ip=_get_user_ip_from_request(request),
        request_url=str(request.url),
    )

    authenticate_and_authorize(auth_context)

    return handler.model_ready(model_name=model_name, model_version=model_version)


@router.get(
    "/health/ready",
    summary="Check if server is ready",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=ServerReadyResponse,
)
def server_ready(
    request: Request,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    bearer_token: str = Depends(security),
) -> ServerReadyResponse:
    """
    Check if the server returns the readiness probe.
    """
    auth_context = PartialAuthContext(
        authz_adapter=authz_adapter,
        bearer_token=bearer_token,
        user_ip=_get_user_ip_from_request(request),
        request_url=str(request.url),
    )

    authenticate_and_authorize(auth_context)

    return handler.server_ready()


@router.get(
    "/health/live",
    summary="Check if server is live",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=ServerLiveResponse,
)
def server_live(
    request: Request,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    bearer_token: str = Depends(security),
) -> ServerLiveResponse:
    """
    Check if the server returns the liveness probe.
    """
    auth_context = PartialAuthContext(
        authz_adapter=authz_adapter,
        bearer_token=bearer_token,
        user_ip=_get_user_ip_from_request(request),
        request_url=str(request.url),
    )

    authenticate_and_authorize(auth_context)

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
    request: Request,
    handler: DefaultHandler = Depends(DefaultHandler),
    authz_adapter: DefaultAdapter = Depends(DefaultAdapter),
    bearer_token: str = Depends(security),
) -> ServerMetadataResponse:
    """
    Retrieve metadata for the server
    """
    auth_context = PartialAuthContext(
        authz_adapter=authz_adapter,
        bearer_token=bearer_token,
        user_ip=_get_user_ip_from_request(request),
        request_url=str(request.url),
    )

    authenticate_and_authorize(auth_context)

    return handler.server_metadata()


def build_inference_response(
    model_name: str,
    request: InferenceRequest,
    result: InferenceResponse,
    model_version: Optional[str] = None,
) -> InferenceResponse:
    """
    Construct an InferenceResponse by encoding a handler’s raw Python result according to content_type
    1. Try per‐output codecs (if request.outputs is set).
    2. Fallback to a request‐level codec (if request.parameters.content_type is set).
    3. Otherwise, echo each result's raw data.
    """
    # Per‐output codec
    outputs: List[ResponseOutput] = []
    for request_output in request.outputs or []:
        output = encode_response_output(result, request_output)
        if output is not None:
            outputs.append(output)

    if outputs:
        return InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            id=request.id,
            outputs=outputs,
        )

    # Request-level codec (only if top-level parameters.content_type was set)
    request_content_type = get_content_type(request)
    if request_content_type:
        response = encode_inference_response(
            model_name=model_name,
            payload=result,
            model_version=model_version,
        )
        if response is not None:
            response.id = request.id
            return response

    # No codec matched - TODO we need to handle the case where the handler and/or request content-type are unknown

    # No content type give in output or requestOutput so just return response data as is
    return result


def _get_user_ip_from_request(request: Request):
    """
    Extracts the user's IP address from the request object, respecting the
    `x-forwarded-for` header if present.
    :param request:  The FastAPI request object
    :return: The IP address of the user
    """
    forwarded = request.headers.get("x-forwarded-for")

    ip = request.client.host

    if forwarded:
        try:
            ip = forwarded.split(",")[0].strip()
        except Exception as e:
            logger.warning(
                f"Request header has x-forwarded-for ({forwarded}), but unable to extract ip.",
                e,
            )

    return ip
