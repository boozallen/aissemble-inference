# aiSSEMBLE Open Inference Protocol FastAPI

The [Open Inference Protocol(OIP)](https://github.com/kserve/open-inference-protocol) specification defines a standard protocol for performing machine learning model inference across serving runtimes for different ML frameworks. This Python application can be leveraged to create FastAPI routes that are compatible with the Open Inference Protocol. By leveraging this library, you get a set to OIP compatible dataplane objects and routes.

## Installation
Add aissemble-open-inference-protocol-fastapi to an application
```bash
pip install aissemble-open-inference-protocol-fastapi
```

## Example of basic usage
Use aissemble-open-inference-protocol-fastapi to create a FastAPI app by creating a file `main.py` with
```python
from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import AissembleOIPFastAPI

app = AissembleOIPFastAPI().app
```

The server will now have a complete set of Open Inference Protocol compatible routes! Ensure you have the fastapi cli tools installed (`pip install "fastapi[standard]"`), then run with:
```bash
fastapi dev main.py
```

View the routes by going to http://127.0.0.1:8000/docs.

## Implementing a Handler
The endpoints will call a [default handler](https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-fastapi/src/aissemble_open_inference_protocol_fastapi/handlers/default_handler.py) that will return 501 not implemented. To make a handler, create your class and extend the abstract base class [dataplane.py](https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-fastapi/src/aissemble_open_inference_protocol_fastapi/handlers/dataplane.py). Then pass your class into the AissembleOIPFastAPI constructor.

### Example of Usage with A Handler
Create your custom handler class with:
```python
from typing import Optional

from aissemble_open_inference_protocol_fastapi.handlers.dataplane import (
    DataplaneHandler,
)
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    MetadataTensor,
    ModelReadyResponse,
    ServerReadyResponse,
    ServerLiveResponse,
    ServerMetadataResponse,
)


class MyHandler(DataplaneHandler):
    def __init__(self):
        super().__init__()

    def infer(
            self,
            payload: InferenceRequest,
            model_name: str,
            model_version: Optional[str] = None,
    ) -> InferenceResponse:
        return InferenceResponse(
            model_name=model_name, model_version=model_version, id="id", outputs=[]
        )

    def model_metadata(
            self,
            model_name: str,
            model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        # Return a stub ModelMetadataResponse
        return ModelMetadataResponse(
            name=model_name,
            versions=[model_version] if model_version else None,
            platform="python",
            inputs=[MetadataTensor(name="input", datatype="FP32", shape=[1])],
            outputs=[
                MetadataTensor(name="output", datatype="FP32", shape=[1])
            ],
        )

    def model_ready(
            self,
            model_name: str,
            model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        # Testing: always ready
        return ModelReadyResponse(name=model_name, ready=True)
    
    def server_ready(
            self,
    ) -> ServerReadyResponse:
        # Testing: always ready
        return ServerReadyResponse(live=True)

    def server_live(
            self,
    ) -> ServerLiveResponse:
        # Testing: always live
        return ServerLiveResponse(live=True)

    def server_metadata(
            self,
    ) -> ServerMetadataResponse:
        # Return a stub ServerMetadataResponse
        return ServerMetadataResponse(
            name="Server",
            version="v2",
            extensions=["extension"],
        )
```

Use aissemble-open-inference-protocol-fastapi to create a FastAPI app and pass it `MyHandler`
```python
from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import AissembleOIPFastAPI

app = AissembleOIPFastAPI(MyHandler).app
```

Now when starting the FastAPI server, the inference request will route to `MyHandler.infer()`

## Features

### Content Type Decoding/Encoding (Work In Progress)
For more information on how to implement content type decoding/encoding, reference the `aissemble-open-inference-protocol-shared` module's [README](../aissemble-open-inference-protocol-shared/README.md)


## Example Usage with Actual ML Model ##
Please see the [example](../examples/fast-api-inference/README.md) folder dedicated for detailed information on how to integrate models with Fast API OIP.