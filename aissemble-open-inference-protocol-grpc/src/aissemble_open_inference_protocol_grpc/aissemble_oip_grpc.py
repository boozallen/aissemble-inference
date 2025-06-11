###
# #%L
# aiSSEMBLE::Open Inference Protocol::FastAPI
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import asyncio
import signal
from concurrent.futures import ThreadPoolExecutor

from grpc import aio
from krausening.logging import LogManager

from aissemble_open_inference_protocol_grpc.grpcInferenceService_pb2_grpc import (
    add_GRPCInferenceServiceServicer_to_server,
)
from aissemble_open_inference_protocol_grpc.grpc_config import GrpcConfig
from aissemble_open_inference_protocol_grpc.inference_servicer import InferenceServicer

HANDLED_SIGNALS = [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]


class AissembleOIPgRPC:
    logger = LogManager.get_instance().get_logger("AissembleOIPgRPC")

    def __init__(self, handler=None, gprc_properties: str = None):
        self.handler = handler
        self.grpc_config = GrpcConfig(gprc_properties)

    async def start(self):
        # Add signal handlers to shut down gracefully
        self._add_terminate_signal_handlers()

        self._create_server()
        self.logger.info("Starting OIP gRPC Server")

        await self._server.start()
        self.logger.info(
            f"gRPC server started at grpc://{self.grpc_config.host}:{self.grpc_config.port}"
        )
        await self._server.wait_for_termination()

    def _create_server(self):
        self._inference_servicer = InferenceServicer(self.handler)
        self._server = aio.server(
            ThreadPoolExecutor(max_workers=self.grpc_config.grpc_workers),
        )
        add_GRPCInferenceServiceServicer_to_server(
            self._inference_servicer, self._server
        )
        self._server.add_insecure_port(
            f"{self.grpc_config.host}:{self.grpc_config.port}"
        )
        return self._server

    def _add_terminate_signal_handlers(self):
        self.logger.info("Adding terminate signal handlers")
        loop = asyncio.get_running_loop()

        for sig in HANDLED_SIGNALS:
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(self.stop()))

    async def stop(self):
        self.logger.info("Stopping OIP GRPC Server")
        await self._server.stop(grace=10)
