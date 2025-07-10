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
    DEFAULT_AUTH_ENABLED = "false"

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

    @property
    def auth_enabled(self) -> bool:
        """
        Whether authorization is enabled for the gRPC server.
        If auth_enabled is set to true with no protected endpoints specified then all endpoints are protected.
        """
        value = self.properties.getProperty("auth_enabled", self.DEFAULT_AUTH_ENABLED)
        environ_override = os.getenv("GRPC_AUTH_ENABLED")
        enabled = environ_override if environ_override else value
        return str(enabled).lower() == "true"

    @property
    def protected_endpoints(self) -> set[str]:
        """
        Returns a set of protected endpoint strings.
        """
        environ_override = os.getenv("GRPC_PROTECTED_ENDPOINTS")
        if environ_override:
            endpoints = [ep.strip() for ep in environ_override.split(",") if ep.strip()]
        else:
            value = self.properties.getProperty("protected_endpoints", "")
            endpoints = [ep.strip() for ep in value.split(",") if ep.strip()]
        return set(endpoints)
