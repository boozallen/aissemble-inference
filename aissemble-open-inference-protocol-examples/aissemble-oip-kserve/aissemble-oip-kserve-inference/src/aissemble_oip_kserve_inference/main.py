###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples KServe Inference
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import numpy as np
from typing import Optional, Union, Dict, Tuple

from tensorflow.keras.models import load_model

from kserve import InferRequest, InferResponse, InferOutput, ModelServer

from aissemble_open_inference_protocol_kserve.aissemble_oip_kserve import (
    AissembleOIPKServe,
)

from aissemble_open_inference_protocol_shared.types.dataplane import (
    Datatype,
)

from aissemble_open_inference_protocol_kserve.kserve_dataplane import (
    KServeDataplaneHandler,
)

""""
This example demonstrates how to use AissembleOIPKServe to create a Kserve model that is compatible with the 
aiSSEMBLE OIP handler. Define the handler the same as how it is for the other aiSSEMBLE OIP solutions, then pass it 
to the AissembleOIPKServe constructor along with the model name. In this example we then load the model and start the server
"""


class CustomKServeDataplaneHandler(KServeDataplaneHandler):
    def __init__(self):
        super().__init__()
        self.ready = False
        self.model = None

    async def infer(
        self,
        model_name: str,
        request: Union[Dict, InferRequest],
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[Union[Dict, InferResponse], Dict[str, str]]:
        keras_model = load_model("model/" + model_name + ".keras")
        # Model will take input data from the payload and make prediction to convert Celsius to Fahrenheit.
        output = keras_model.predict(np.array(request.inputs[0].data))
        # Need to convert to list so that we are align with output format.
        output_list = output.tolist()
        response_headers = {}
        return InferResponse(
            response_id=request.id,
            model_name=model_name,
            infer_outputs=[
                InferOutput(
                    name=model_name,
                    shape=request.inputs[0].shape,
                    datatype=Datatype.FP32,
                    data=output_list,
                )
            ],
        ), response_headers

    async def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> Dict:
        load_model("model/" + model_name + ".keras")
        input_tensors = []
        for input in self.model.inputs:
            datatype = None
            if input.dtype == "float32":
                datatype = "FP32"
            input_dict = {
                "name": "input",
                "datatype": datatype,
                "shape": [input.shape[1]],
            }
            input_tensors.append(input_dict)
        output_tensors = []
        for output in self.model.outputs:
            datatype = None
            if output.dtype == "float32":
                datatype = "FP32"
            output_dict = {
                "name": "output",
                "datatype": datatype,
                "shape": [output.shape[1]],
            }
            output_tensors.append(output_dict)
        return {
            "name": model_name,
            "platform": "python",
            "inputs": input_tensors,
            "outputs": output_tensors,
        }

    async def model_ready(
        self, model_name: str, disable_predictor_health_check: bool = False
    ) -> bool:
        return True

    def model_load(self, model_name) -> bool:
        self.model = load_model("model/" + model_name + ".keras")
        self.ready = True
        return True


if __name__ == "__main__":
    model_name = "convert_celsius_to_fahrenheit"
    oip_kserve = AissembleOIPKServe(name=model_name, handler=CustomKServeDataplaneHandler())
    # model needs to be loaded before server start
    oip_kserve.load()
    oip_kserve.start_server()