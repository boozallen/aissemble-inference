# aiSSEMBLE Open Inference Protocol gRPC

The [Open Inference Protocol(OIP)](https://github.com/kserve/open-inference-protocol) specification defines a standard protocol for performing machine learning model inference across serving runtimes for different ML frameworks. This Python application can be leveraged to create a gRPC server that is compatible with the Open Inference Protocol. It handles standing up and tearing down the server so you only need to worry about the inferencing functionality.

## Installation
Add aissemble-open-inference-protocol-grpc to an application
```bash
pip install aissemble-open-inference-protocol-grpc
```

## Usage

### Creating the Server
Use aissemble-open-inference-protocol-grpc to create a gRPC server by creating a file `main.py` with:
```python
import asyncio
from aissemble_open_inference_protocol_grpc.aissemble_oip_grpc import AissembleOIPgRPC

grpc = AissembleOIPgRPC()

if __name__ == '__main__':
    asyncio.run(grpc.start())
```
The gRPC server will come up after a few seconds and will be OIP compliant. The proto specifications can be found in the [grpcInferenceService.proto](proto/grpcInferenceService.proto) file. 

### Implementing the Endpoints
By default, the gRPC endpoints will return a Method Not Implemented. TODO on how users can implement their functions with the endpoints 

## Configuration
There are several configurations available that affect the sever. These can be implemented with the (TODO update with aissemble config library). You can also set them via environment variables.

| Configuration name | default value | description                                                                    |
|--------------------|---------------|--------------------------------------------------------------------------------|
| grpc_host          | 0.0.0.0       | The host the grpc server will start on                                         |
| grpc_port          | 8080          | The port the grpc server will start on                                         |
| grpc_workers       | 3             | Number of workers to be used by the server to execute non-AsyncIO RPC handlers |

