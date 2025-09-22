###
# #%L
# aiSSEMBLE::Open Inference Protocol::Shared
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from abc import ABC, abstractmethod

from aissemble_open_inference_protocol_shared.auth.auth_adapter_base import (
    AuthAdapterBase,
)
from aissemble_open_inference_protocol_shared.config.oip_config import OIPConfig
from aissemble_open_inference_protocol_shared.handlers.dataplane import (
    DataplaneHandler,
)
from aissemble_open_inference_protocol_shared.handlers.model_handler import (
    ModelHandler,
    DefaultModelHandler,
)


class AissembleOIPService(ABC):
    """
    Abstract class for all aiSSEMBLE Open Inference Protocol solutions. Defines required standardization.
    """

    def __init__(
        self,
        adapter: AuthAdapterBase | None,
        model_handler: ModelHandler = DefaultModelHandler(),
    ):
        super(AissembleOIPService, self).__init__()
        self.config = OIPConfig()
        self.model_handler = model_handler
        self.dataplane_handler = DataplaneHandler(self.model_handler)
        self.adapter = adapter
        self.server = None

    def model_load(self, model_name: str) -> bool:
        return self.model_handler.model_load(model_name)

    @abstractmethod
    async def start_server(self):
        pass
