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
To make a custom handler to integrate with Kserve, create your class and extend the [DataplaneHandler](https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-shared/src/aissemble_open_inference_protocol_shared/handlers/dataplane.py).
Then, implement methods based on the model such as load and infer.

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
    Datatype,
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
            inputs=[MetadataTensor(name="input", datatype=Datatype.FP32, shape=[1])],
            outputs=[
                MetadataTensor(name="output", datatype=Datatype.FP32, shape=[1])
            ],
        )

    def model_load(self, model_name: str) -> bool:
        # Do some model loading
        return True
```
You can now use this handler to create the AissembleOIPKServe class to be loaded into the Kserve inferencing server
Example Kserve inferencing server
```python
from aissemble_open_inference_protocol_kserve.aissemble_oip_kserve import (
    AissembleOIPKServe,
)

if __name__ == "__main__":
    model_name = "my_model"
    oip_kserve = AissembleOIPKServe(name=model_name, handler=MyHandler())
    oip_kserve.model_load(model_name=model_name)
    oip_kserve.start()
```

You are now ready to containerize the app and pass it to the Kserve Kubernetes resources.

## Configurations
There are several configurations available that affect the server. These can be implemented via [Krausening](https://github.com/TechnologyBrewery/krausening/blob/dev/README.md) properties file `oip.properties` or environment variables.

| Configuration Name              | Environment Variable            | Default Value | Description                                                                                                                        |
|---------------------------------|---------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------|
| `kserve_http_port`              | `KSERVE_HTTP_PORT`              | 8080          | The HTTP Port listened to by the model server                                                                                      |
| `kserve_grpc_port`              | `KSERVE_GRPC_PORT`              | 8081          | The gRPC Port listened to by the model server                                                                                      |
| `kserve_workers`                | `KSERVE_WORKERS`                | 1             | The number of uvicorn workers for multi-processing                                                                                 |
| `kserve_max_threads`            | `KSERVE_MAX_THREADS`            | 4             | The max number of gRPC processing threads                                                                                          |
| `kserve_max_asyncio_workers`    | `KSERVE_MAX_ASYNCIO_WORKERS`    | None          | The max number of asyncio workers to spawn                                                                                         |
| `kserve_enable_grpc`            | `KSERVE_ENABLE_GRPC`            | True          | Enable gRPC for the model server                                                                                                   |
| `kserve_enable_docs_url`        | `KSERVE_ENABLE_DOCS_URL`        | False         | Enable docs url '/docs' to display Swagger UI                                                                                      |
| `kserve_enable_latency_logging` | `KSERVE_ENABLE_LATENCY_LOGGING` | True          | Enable a log line per request with preprocess/predict/postprocess latency metrics                                                  |
| `kserve_access_log_format`      | `KSERVE_ACCESS_LOG_FORMAT`      | None          | The asgi access logging format. It allows to override only the `uvicorn.access`'s format configuration with a richer set of fields |
| `kserve_grace_period`           | `KSERVE_GRACE_PERIOD`           | 30            | The grace period in seconds to wait for the server to stop                                                                         |

## Additional Configuration
Additional configuration options may be available via command-line arguments. See the [KServe documentation](https://kserve.github.io/website/docs/intro) for more details.

## Examples
For working examples, refer to the [Examples](https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-examples/README.md#kserve) documentation.
