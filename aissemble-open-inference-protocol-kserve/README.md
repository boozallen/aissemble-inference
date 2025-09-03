# aiSSEMBLE Open Inference Protocol&trade; KServe

The [Open Inference Protocol (OIP)](https://github.com/kserve/open-inference-protocol) specification defines a standard protocol for performing machine learning model inference across serving runtimes for different ML frameworks. This Python application can be leveraged to deploy KServe that are compatible with the Open Inference Protocol.

## Installation
Add `aissemble-open-inference-protocol-kserve` to an application
```bash
pip install aissemble-open-inference-protocol-kserve
```

## Usage
### Prerequisite
In order to stand up KServe Using aiSSEMBLE Open Inference Protocol, user should make sure all infrastructure/environment for KServe is set up using the [official Documentation](https://kserve.github.io/website/docs/intro).
Once KServe environment is set up, user can proceed with implementing custom handler for KServe using aiSSEMBLE Open Inference Protocol.

### Implementing a Handler
To make a custom handler to integrate with kserve, create your handler class and extend the [AissembleOIPKServe](https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-kserve/src/aissemble_open_inference_protocol_kserve/aissemble_oip_kserve.py).
Then, implement methods based on the model's need such as load() for loading a model, and optional transformer such as preprocess() and/or postprocess() that transform input or output data for client and prediction model.
predict method will call infer method of dataplaneHandler in which you need to implement either with [REST](../aissemble-open-inference-protocol-fastapi/README.md) or [gRPC](../aissemble-open-inference-protocol-grpc/README.md)

### Example of Usage with a Handler
Create your custom handler class with:
```python
from kserve import ModelServer
from typing import Optional
from aissemble_open_inference_protocol_kserve.aissemble_oip_kserve import (
    AissembleOIPKServe,
)

from aissemble_open_inference_protocol_shared.handlers.dataplane import DataplaneHandler
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
    MetadataTensor,
    ResponseOutput,
    Datatype,
)


class CustomDataplaneHandler(DataplaneHandler):
    def __init__(self):
        super().__init__()

    def infer(
            self,
            payload: InferenceRequest,
            model_name: str,
            model_version: Optional[str] = None,
    ) -> InferenceResponse:
        # your dataplane prediction logic goes here
        output_list = []
        return InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            id=payload.id,
            outputs=[
                ResponseOutput(
                    name=model_name,
                    shape=payload.inputs[0].shape,
                    datatype=Datatype.FP32,
                    data=output_list,
                )
            ],
        )

    def model_metadata(
            self,
            model_name: str,
            model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        # your model metadata logic goes here. 
        your_input_tensor = []
        your_output_tensor = []
        return ModelMetadataResponse(
            name=model_name,
            versions=[model_version] if model_version else None,
            platform="python",
            inputs=your_input_tensor,
            outputs=your_output_tensor,
        )

    def model_ready(
            self,
            model_name: str,
            model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        try:
            # your model ready logic goes here.
            return ModelReadyResponse(name=model_name, ready=True)
        except ValueError:
            return ModelReadyResponse(name=model_name, ready=False)



class KserveCustomHandler(AissembleOIPKServe):
    """
    Implements Custom predictor of AissembleOIPKServe for requesting model.
    handler refers to custom DataplaneHandler
    """
    def __init__(self, name: str, model_path: str, handler=None):
        super().__init__(name, handler)
        self.model = None
        self.name = name
        self.model_path = model_path
        self.handler = handler

    def preprocess(self):
        """As preprocess is optional API in KServe, it is up to user to implement preprocess based on their use case to transform raw input to the format expected for model serve if applicable."""
    pass
    
    def postprocess(self):
        """As postprocess is optional API in KServe, it is up to user to implement preprocess based on their use case to transform prediction output to the format expected for client if applicable."""
        pass

    def load(self):
        """As loading model is different for each client, it is up to user to implement load based on their use case. 
        NOTE: setting self.ready to True will make sure KServe Model is ready to serve."""
        self.ready = True
        return self.ready

    async def start(self):
        self.load()
        ModelServer().start([self])

if __name__ == "__main__":
    """ CustomDataPlaneHandler is extending from DataplaneHandler abstract base class, user should be extending this DataplaneHandler for their implementation of model prediction as you can see from CustomDataPlaneHandler.
    """
    model = KserveCustomHandler( name= "sample_model",
        model_path="sample_model_path",
        handler=CustomDataplaneHandler,
    )
    model.load()
    model.start()
```

Once you built your custom image for python application for KServe and KServe setup is complete, then you can run prediction based on preferred API calls (REST or gRPC)

## Examples
For working examples, refer to the [Examples](https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-examples/README.md#kserve) documentation.