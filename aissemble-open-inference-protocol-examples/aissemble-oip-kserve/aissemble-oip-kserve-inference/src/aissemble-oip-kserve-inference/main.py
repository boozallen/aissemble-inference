###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples KServe Inference
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from kserve import ModelServer
from tensorflow.keras.models import load_model

from krausening.logging import LogManager

from aissemble_open_inference_protocol_kserve.aissemble_oip_kserve import (
    AissembleOIPKServe,
)

from aissemble_open_inference_protocol_shared.handlers.dataplane import DataplaneHandler

""""
AissembleOIPKServe is base class for Kserve Handler that implements predict method. (Other methods will be implemented soon) 
If user wants to use what AissembleOIPKServe offers there is no need to create custom class and we can just make AissembleOIPKServe instance. 
If user somehow wants to implement custom logic for prediction or load, user can extend AissembleOIPKServe with custom logic to override it.
In this case, only load is overridden and predict method will be used from AissembleOIPKServe class
"""


class KserveCustomModel(AissembleOIPKServe):
    """
    Implements Custom predictor of AissembleOIPKServe for requesting model.
    """

    logger = LogManager.get_instance().get_logger("KserveCustomModel")

    def __init__(self, name: str, model_path: str, handler=None):
        super().__init__(name, handler)
        self.model = None
        self.name = name
        self.model_path = model_path
        self.handler = handler

    def load(self):
        self.model = load_model("model/" + self.model_path + ".keras")
        self.ready = True
        self.logger.info("Kserve Custom Model Loaded Successfully.")


if __name__ == "__main__":
    # DataplaneHandler is abstract base class, user should be extending this class for their implementation based on preferred API calls (REST or GRPC)
    model = KserveCustomModel(
        "kserve-model", "convert_celsius_to_fahrenheit", DataplaneHandler
    )
    model.load()
    ModelServer().start([model])
