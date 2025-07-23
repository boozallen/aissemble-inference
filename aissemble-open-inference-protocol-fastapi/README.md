# aiSSEMBLE Open Inference Protocol&trade; FastAPI

The [Open Inference Protocol (OIP)](https://github.com/kserve/open-inference-protocol) specification defines a standard protocol for performing machine learning model inference across serving runtimes for different ML frameworks. This Python application can be leveraged to create FastAPI routes that are compatible with the Open Inference Protocol.

## Installation
Add `aissemble-open-inference-protocol-fastapi` to an application
```bash
pip install aissemble-open-inference-protocol-fastapi
```

## Usage
Use `aissemble-open-inference-protocol-fastapi` to create a FastAPI app by creating a file `main.py` with
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
The endpoints will call a [default handler](https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-shared/src/aissemble_open_inference_protocol_shared/handlers/default_handler.py) that will return 501 Not Implemented. To make a handler, create your class and extend the abstract base method [dataplane.py](https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-shared/src/aissemble_open_inference_protocol_shared/handlers/dataplane.py). Then pass your class into the `AissembleOIPFastAPI` constructor.

### Example of Usage with a Handler
Create your custom handler class with:
```python
from typing import Optional

from aissemble_open_inference_protocol_shared.handlers.dataplane import (
    DataplaneHandler,
)
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    MetadataTensor,
    ModelReadyResponse,
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
```

Use `aissemble-open-inference-protocol-fastapi` to create a FastAPI app and pass it `MyHandler`
```python
from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import AissembleOIPFastAPI

app = AissembleOIPFastAPI(MyHandler).app
```

Now when starting the FastAPI server, the inference request will route to `MyHandler.infer()`


## Configurations
There are several configurations available that affect the server. These can be implemented via [Krausening](https://github.com/TechnologyBrewery/krausening/blob/dev/README.md) or environment variables.

| Configuration Name     | Environment Variable       | Default Value              | Description                                                                |
|------------------------|----------------------------|----------------------------|----------------------------------------------------------------------------|
| `auth_secret`          | `AUTH_SECRET`              | None                       | The secret key used to decode jwt token                                    |
| `auth_algorithm`       | `AUTH_ALGORITHM`           | HS256                      | The algorithm used to decode jwt tokens                                    |
| `pdp_url`              | `OIP_PDP_URL`              | http://localhost:8080/pdp  | The URL of the Policy Decision Point (PDP) used for authorization checks   |

## Examples
For working examples, refer to the [Examples](https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-examples/README.md#fastapi) documentation.