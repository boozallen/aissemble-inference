###
# #%L
# aiSSEMBLE::Open Inference Protocol::KServe
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from kserve import Model, ModelServer

from aissemble_open_inference_protocol_kserve.kserve_dataplane import (
    KServeDataplaneAdapter,
)
from aissemble_open_inference_protocol_shared.aissemble_oip_service import (
    AissembleOIPService,
)
from aissemble_open_inference_protocol_shared.handlers.model_handler import ModelHandler


class AissembleOIPKServe(Model, AissembleOIPService):
    def __init__(
        self,
        name: str,
        model_handler: ModelHandler,
    ):
        Model.__init__(self, name)
        AissembleOIPService.__init__(self, adapter=None, model_handler=model_handler)

        # TODO now that we have abstracted the dataplane handler from the user, this model should be used instead of
        #  overriding Kserve's dph
        # Create a Kserve dataplane adapter to route requests to users model data.
        self.kserve_dataplane_adapter = KServeDataplaneAdapter(
            handler=self.dataplane_handler
        )
        self.model = None
        # initialize model ready false
        self.ready = False

    def load(self) -> bool:
        # update the model ready flag based on model_load() result
        self.ready = self.dataplane_handler.model_load(self.name)
        return self.ready

    def start_server(self):
        model_server = ModelServer(
            http_port=self.config.kserve_http_port,
            grpc_port=self.config.kserve_grpc_port,
            workers=self.config.kserve_workers,
            max_threads=self.config.kserve_max_threads,
            max_asyncio_workers=self.config.kserve_max_asyncio_workers,
            enable_grpc=self.config.kserve_enable_grpc,
            enable_docs_url=self.config.kserve_enable_docs_url,
            enable_latency_logging=self.config.kserve_enable_latency_logging,
            access_log_format=self.config.kserve_access_log_format,
        )
        model_server.dataplane = self.kserve_dataplane_adapter
        model_server.start([self])
