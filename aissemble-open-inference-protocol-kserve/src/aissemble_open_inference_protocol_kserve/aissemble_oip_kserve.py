###
# #%L
# aiSSEMBLE::Open Inference Protocol::KServe
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from kserve import Model, InferRequest, InferResponse, ModelServer

from aissemble_open_inference_protocol_kserve.mappers.infer_mapper import InferMapper
from aissemble_open_inference_protocol_shared.aissemble_oip_service import (
    AissembleOIPService,
)
from aissemble_open_inference_protocol_shared.handlers.dataplane import (
    DataplaneHandler,
    DefaultHandler,
)


class AissembleOIPKServe(Model, AissembleOIPService):
    def __init__(self, name: str, handler: DataplaneHandler = DefaultHandler()):
        Model.__init__(self, name)
        AissembleOIPService.__init__(self, handler=handler, adapter=None)
        self.model = None

    def predict(
        self,
        payload: InferRequest,
        headers: dict[str, str] = None,
        response_headers: dict[str, str] = None,
    ) -> InferResponse:
        inference_request = InferMapper.infer_request_to_inference_request(payload)
        inference_response = self.handler.infer(
            payload=inference_request,
            model_name=payload.model_name,
            model_version=payload.model_version,
        )

        infer_response = InferMapper.inference_response_to_infer_response(
            inference_response
        )
        return infer_response

    def load(self) -> bool:
        return self.handler.model_load(self.name)

    def start(self):
        ModelServer(
            http_port=self.config.kserve_http_port,
            grpc_port=self.config.kserve_grpc_port,
            workers=self.config.kserve_workers,
            max_threads=self.config.kserve_max_threads,
            max_asyncio_workers=self.config.kserve_max_asyncio_workers,
            enable_grpc=self.config.kserve_enable_grpc,
            enable_docs_url=self.config.kserve_enable_docs_url,
            enable_latency_logging=self.config.kserve_enable_latency_logging,
            access_log_format=self.config.kserve_access_log_format,
            grace_period=self.config.kserve_grace_period,
        ).start([self])
