###
# #%L
# aiSSEMBLE::Open Inference Protocol::gRPC
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import os

from krausening.properties import PropertyManager


class GrpcConfig:
    DEFAULT_GRPC_HOST = "0.0.0.0"
    DEFAULT_GRPC_PORT = "8080"
    DEFAULT_GRPC_WORKERS = "3"

    def __init__(self, properties_file: str) -> None:
        self.properties = PropertyManager.get_instance().get_properties(properties_file)

    @property
    def host(self) -> str:
        value = self.properties.getProperty("grpc_host", self.DEFAULT_GRPC_HOST)
        environ_override = os.getenv("GRPC_HOST")
        return environ_override if environ_override else value

    @property
    def port(self) -> str:
        value = self.properties.getProperty("grpc_port", self.DEFAULT_GRPC_PORT)
        environ_override = os.getenv("GRPC_PORT")
        return environ_override if environ_override else value

    @property
    def grpc_workers(self) -> int:
        value = self.properties.getProperty("grpc_workers", self.DEFAULT_GRPC_WORKERS)
        environ_override = os.getenv("GRPC_WORKERS")
        worker_count = environ_override if environ_override else value
        return int(worker_count)
