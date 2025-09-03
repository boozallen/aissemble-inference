from tensorflow.keras.models import load_model

from aissemble_open_inference_protocol_kserve.aissemble_oip_kserve import (
    AissembleOIPKServe,
)


class KserveCustomHandler(AissembleOIPKServe):
    """
    Implements Custom predictor of AissembleOIPKServe for requesting model.
    """

    def __init__(self, name: str, model_path: str, handler=None):
        super().__init__(name, handler)
        self.model = None
        self.name = name
        self.model_path = model_path
        self.handler = handler
        self.ready = False

    def model_load(self, model_name: str = None):
        self.model = load_model("tests/resources/" + self.model_path + ".keras")
        self.ready = True
