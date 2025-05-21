###
# #%L
# aiSSEMBLE::Open Inference Protocol::FastAPI
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###

from fastapi import FastAPI

from aissemble_open_inference_protocol_fastapi.handlers.default_handler import (
    DefaultHandler,
)
from aissemble_open_inference_protocol_fastapi.rest import endpoints


class AissembleOIPFastAPI:

    def __init__(self, handler=None):
        self.app = FastAPI()
        self.app.include_router(endpoints.router)
        if handler is not None:
            self.app.dependency_overrides[DefaultHandler] = handler
