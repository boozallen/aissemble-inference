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
    """## performs inference on a model.

    Returns: the prediction results
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
    """## performs inference on a model given a specific version.

    Returns: the prediction results
    """
    return handler.infer(
        model_name=model_name, model_version=model_version, payload=payload
    )
