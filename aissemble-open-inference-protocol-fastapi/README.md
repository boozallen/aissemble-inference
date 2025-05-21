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

## Implementing Inference Handler
The endpoints will call a [default handler](src/aissemble_open_inference_protocol_fastapi/handlers/default_handler.py) that will return 501 not implemented. To make a handler, create your class and extend the abstract base class [dataplane.py](src/aissemble_open_inference_protocol_fastapi/handlers/dataplane.py). Then just pass your class into our AissembleOIPFastAPI constructor.

### Example of Usage with A Handler
Create your custom handler class with:
```python
from typing import Optional
from aissemble_open_inference_protocol_fastapi.handlers.dataplane import DataplaneHandler
from aissemble_open_inference_protocol_fastapi.types.dataplane import InferenceRequest, InferenceResponse

class MyHandler(DataplaneHandler):
    def __init__(self):
        super().__init__()

    def infer(
            self,
            payload: InferenceRequest,
            model_name: str,
            model_version: Optional[str] = None,
    ) -> InferenceResponse:
        return InferenceResponse(model_name=model_name, model_version=model_version, outputs=[])
```

Use aissemble-open-inference-protocol-fastapi to create a FastAPI app and pass it `MyHandler`
```python
from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import AissembleOIPFastAPI

app = AissembleOIPFastAPI(MyHandler).app
```

Now when starting the FastAPI server, the inference request will route to `MyHandler.infer()`
