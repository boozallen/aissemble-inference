###
# #%L
# aiSSEMBLE::Open Inference Protocol::KServe
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from kserve import Model, InferRequest, InferResponse

from aissemble_open_inference_protocol_kserve import InferMapper


class AissembleOIPKServe(Model):
    def __init__(self, name: str, handler=None):
        super().__init__(name)
        self.name = name
        self.model = None
        self.handler = handler

    def predict(
        self,
        payload: InferRequest,
        headers: dict[str, str] = None,
        response_headers: dict[str, str] = None,
    ) -> InferResponse:
        inference_request = InferMapper.infer_request_to_inference_request(payload)
        inference_response = self.handler.infer(
            self,
            payload=inference_request,
            model_name=payload.model_name,
            model_version=payload.model_version,
        )

        infer_response = InferMapper.inference_response_to_infer_response(
            inference_response
        )

        return infer_response
