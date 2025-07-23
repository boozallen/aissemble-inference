# aiSSEMBLE Open Inference Protocol gRPC Inference Example

This example demonstrates how to implement custom handlers for all Open Inference Protocol gRPC endpoints. The example shows how to create a gRPC server that supports mathematical operations on input data.

## Running the Example

### 1. Build and install dependencies to prepare the gRPC server by running the following Poetry command:
```sh
poetry install
```

### 2. Start the gRPC server using the following command:
```sh
poetry run run_server
```
The server will start on `grpc://0.0.0.0:8080`

### 3. Run the following grpcurl commands to test the different endpoints:
- [grpcurl installation instructions](https://github.com/fullstorydev/grpcurl?tab=readme-ov-file#installation)

| API             | Command                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Inference       | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>-d '{<br/>"model_name": "default",<br/>"model_version": "1.0",<br/>"id": "test_request",<br/>"inputs": [{<br/>"name": "input",<br/>"datatype": "FP32",<br/>"shape": [3],<br/>"contents": {"fp32_contents": [1.0,3.0,5.0]}<br/>}],<br/>"outputs": [{"name": "output"}]<br/>}' \\<br/>localhost:8080 inference.GrpcInferenceService/ModelInfer</pre> |
| Model Metadata  | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>-d '{"name": "default", "version": "1.0"}' \\<br/>localhost:8080 inference.GrpcInferenceService/ModelMetadata</pre>                                                                                                                                                                                                                                |
| Server Ready    | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>localhost:8080 inference.GrpcInferenceService/ServerReady</pre>                                                                                                                                                                                                                                                                                    |
| Server Live     | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>localhost:8080 inference.GrpcInferenceService/ServerLive</pre>                                                                                                                                                                                                                                                                                     |
| Server Metadata | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>localhost:8080 inference.GrpcInferenceService/ServerMetadata</pre>                                                                                                                                                                                                                                                                                 |
| Model Ready     | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>-d '{"name": "default", "version": "1.0"}' \\<br/>localhost:8080 inference.GrpcInferenceService/ModelReady</pre>                                                                                                                                                                                                                                   |
