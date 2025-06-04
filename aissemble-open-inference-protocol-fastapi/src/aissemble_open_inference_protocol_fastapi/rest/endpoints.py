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

from aissemble_open_inference_protocol_fastapi.handlers.default_handler import (
    DefaultHandler,
)
from aissemble_open_inference_protocol_fastapi.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelMetadataErrorResponse,
    ModelReadyResponse,
)

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
) -> InferenceResponse:
    """
    Perform inference using the specified model and return the prediction results.
    """
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
) -> InferenceResponse:
    """
    Perform inference using the specified model version and return the prediction results.
    """
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
) -> ModelMetadataResponse:
    """
    Retrieve metadata for the specified model.
    """
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
) -> ModelMetadataResponse:
    """
    Retrieve metadata for the specified model version.
    """
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
) -> ModelReadyResponse:
    """
    Check if the specified model is ready to serve requests.
    """
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
) -> ModelReadyResponse:
    """
    Check if the specified model version is ready to serve requests.
    """
    return handler.model_ready(model_name=model_name, model_version=model_version)
