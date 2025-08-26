###
# #%L
# aiSSEMBLE::Open Inference Protocol::Shared
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import os
from typing import Optional

from krausening.properties import PropertyManager


class OIPConfig:
    """
    Configurations for OIP
    """

    DEFAULT_ALGORITHM = "HS256"
    DEFAULT_PDP_URL = "http://localhost:8080/pdp"

    DEFAULT_GRPC_HOST = "0.0.0.0"
    DEFAULT_GRPC_PORT = "8081"
    DEFAULT_GRPC_WORKERS = "3"
    DEFAULT_AUTH_ENABLED = "true"

    DEFAULT_FASTAPI_HOST = "127.0.0.1"
    DEFAULT_FASTAPI_PORT = "8082"
    DEFAULT_FASTAPI_RELOAD = "True"

    DEFAULT_KSERVE_HTTP_PORT = "8080"
    DEFAULT_KSERVE_GRPC_PORT = "8081"
    DEFAULT_KSERVE_WORKERS = "1"
    DEFAULT_KSERVE_MAX_THREADS = "4"
    DEFAULT_KSERVE_MAX_ASYNCIO_WORKERS = ""  # Represents None
    DEFAULT_KSERVE_ENABLE_GRPC = "True"
    DEFAULT_KSERVE_ENABLE_DOCS_URL = "False"
    DEFAULT_KSERVE_ENABLE_LATENCY_LOGGING = "True"
    DEFAULT_KSERVE_ACCESS_LOG_FORMAT = ""  # Represents None
    DEFAULT_KSERVE_GRACE_PERIOD = "30"

    def __init__(self):
        self.properties = PropertyManager.get_instance().get_properties(
            "oip.properties"
        )

    #########################
    # Authorization
    #########################

    @property
    def auth_enabled(self) -> bool:
        """
        Whether authorization is enabled for the server.
        If auth_enabled is set to true with no protected endpoints specified then all endpoints are protected.
        """
        value = self.properties.getProperty("auth_enabled", self.DEFAULT_AUTH_ENABLED)
        environ_override = os.getenv("AUTH_ENABLED")
        enabled = environ_override if environ_override else value
        return str(enabled).lower() == "true"

    def auth_secret(self):
        """
        Returns the auth secret key
        """
        value = self.properties.getProperty("auth_secret", "")
        environ_override = os.getenv("AUTH_SECRET")
        return environ_override if environ_override else value

    def auth_algorithm(self):
        """
        Returns the auth algorithm
        """
        value = self.properties.getProperty("auth_algorithm", self.DEFAULT_ALGORITHM)
        environ_override = os.getenv("AUTH_ALGORITHM")
        return environ_override if environ_override else value

    def pdp_url(self):
        """
        Returns the PDP url
        """
        value = self.properties.getProperty("pdp_url", self.DEFAULT_PDP_URL)
        environ_override = os.getenv("OIP_PDP_URL")
        return environ_override if environ_override else value

    #########################
    # gRPC
    #########################
    @property
    def grpc_host(self) -> str:
        value = self.properties.getProperty("grpc_host", self.DEFAULT_GRPC_HOST)
        environ_override = os.getenv("GRPC_HOST")
        return environ_override if environ_override else value

    @property
    def grpc_port(self) -> str:
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
    def grpc_protected_endpoints(self) -> set[str]:
        """
        Returns a set of protected endpoint strings.
        """
        environ_override = os.getenv("GRPC_PROTECTED_ENDPOINTS")
        if environ_override:
            endpoints = [ep.strip() for ep in environ_override.split(",") if ep.strip()]
        else:
            value = self.properties.getProperty("grpc_protected_endpoints", "")
            endpoints = [ep.strip() for ep in value.split(",") if ep.strip()]
        return set(endpoints)

    #########################
    # FastAPI
    #########################
    # , reload=reload, host=host, port=port
    @property
    def fastapi_host(self) -> str:
        value = self.properties.getProperty("fastapi_host", self.DEFAULT_FASTAPI_HOST)
        environ_override = os.getenv("FASTAPI_HOST")
        return environ_override if environ_override else value

    @property
    def fastapi_port(self) -> int:
        value = self.properties.getProperty("fastapi_port", self.DEFAULT_FASTAPI_PORT)
        environ_override = os.getenv("FASTAPI_PORT")
        return int(environ_override if environ_override else value)

    @property
    def fastapi_reload(self) -> bool:
        value = self.properties.getProperty(
            "fastapi_reload", self.DEFAULT_FASTAPI_RELOAD
        )
        environ_override = os.getenv("FASTAPI_RELOAD")
        return bool(environ_override if environ_override else value)

    #########################
    # Kserve
    #########################

    @property
    def kserve_http_port(self) -> int:
        """
        The HTTP Port listened to by the model server.
        """
        value = self.properties.getProperty(
            "kserve_http_port", self.DEFAULT_KSERVE_HTTP_PORT
        )
        environ_override = os.getenv("KSERVE_HTTP_PORT")
        return int(environ_override if environ_override else value)

    @property
    def kserve_grpc_port(self) -> int:
        """
        The GRPC Port listened to by the model server.
        """
        value = self.properties.getProperty(
            "kserve_grpc_port", self.DEFAULT_KSERVE_GRPC_PORT
        )
        environ_override = os.getenv("KSERVE_GRPC_PORT")
        return int(environ_override if environ_override else value)

    @property
    def kserve_workers(self) -> int:
        """
        Number of uvicorn workers for multiprocessing.
        """
        value = self.properties.getProperty(
            "kserve_workers", self.DEFAULT_KSERVE_WORKERS
        )
        environ_override = os.getenv("KSERVE_WORKERS")
        return int(environ_override if environ_override else value)

    @property
    def kserve_max_threads(self) -> int:
        """
        Max number of gRPC processing threads.
        """
        value = self.properties.getProperty(
            "kserve_max_threads", self.DEFAULT_KSERVE_MAX_THREADS
        )
        environ_override = os.getenv("KSERVE_MAX_THREADS")
        return int(environ_override if environ_override else value)

    @property
    def kserve_max_asyncio_workers(self) -> Optional[int]:
        """
        Max number of AsyncIO threads. Default returns `None`.
        """
        value = self.properties.getProperty(
            "kserve_max_asyncio_workers", self.DEFAULT_KSERVE_MAX_ASYNCIO_WORKERS
        )
        environ_override = os.getenv("KSERVE_MAX_ASYNCIO_WORKERS")
        final_value = environ_override or value
        return int(final_value) if final_value else None

    @property
    def kserve_enable_grpc(self) -> bool:
        """
        Whether to enable gRPC for the model server.
        """
        value = self.properties.getProperty(
            "kserve_enable_grpc", self.DEFAULT_KSERVE_ENABLE_GRPC
        )
        environ_override = os.getenv("KSERVE_ENABLE_GRPC")
        enable_grpc = environ_override if environ_override else value
        return str(enable_grpc).lower() == "true"

    @property
    def kserve_enable_docs_url(self) -> bool:
        """
        Whether to enable docs url '/docs' to display Swagger UI.
        """
        value = self.properties.getProperty(
            "kserve_enable_docs_url", self.DEFAULT_KSERVE_ENABLE_DOCS_URL
        )
        environ_override = os.getenv("KSERVE_ENABLE_DOCS_URL")
        enable_docs = environ_override if environ_override else value
        return str(enable_docs).lower() == "true"

    @property
    def kserve_enable_latency_logging(self) -> bool:
        """
        Whether to enable latency logging for requests.
        """
        value = self.properties.getProperty(
            "kserve_enable_latency_logging", self.DEFAULT_KSERVE_ENABLE_LATENCY_LOGGING
        )
        environ_override = os.getenv("KSERVE_ENABLE_LATENCY_LOGGING")
        enable_logging = environ_override if environ_override else value
        return str(enable_logging).lower() == "true"

    @property
    def kserve_access_log_format(self) -> Optional[str]:
        """
        Format to set for the access log (provided by asgi-logger). Default returns `None`.
        """
        value = self.properties.getProperty(
            "kserve_access_log_format", self.DEFAULT_KSERVE_ACCESS_LOG_FORMAT
        )
        environ_override = os.getenv("KSERVE_ACCESS_LOG_FORMAT")
        final_value = environ_override or value
        return final_value if final_value else None

    @property
    def kserve_grace_period(self) -> int:
        """
        The grace period in seconds to wait for the server to stop.
        """
        value = self.properties.getProperty(
            "kserve_grace_period", self.DEFAULT_KSERVE_GRACE_PERIOD
        )
        environ_override = os.getenv("KSERVE_GRACE_PERIOD")
        return int(environ_override if environ_override else value)
