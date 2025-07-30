[[Return to Examples Documentation]](../../README.md)

# aiSSEMBLE Open Inference Protocol&trade; gRPC Inference Example

This example demonstrates how to implement custom handlers for all Open Inference Protocol gRPC endpoints. The example shows how to create a gRPC server that supports mathematical operations on input data.

## Getting Started
- Ensure you have `grpcurl` installed. If not, follow the [grpcurl installation instructions](https://github.com/fullstorydev/grpcurl?tab=readme-ov-file#installation)
- Ensure you have Poetry installed. If not, follow the [Poetry installation guide](https://python-poetry.org/docs/#installation)
- Build and install all dependencies to prepare the gRPC server by running the following Poetry command:
    ```bash
    poetry install
    ```

## Running the Example

1. Start the gRPC server using the following command:
    ```sh
    poetry run run_server
    ```
    The server will start on `grpc://0.0.0.0:8080`


2. Run the following `grpcurl` commands to test the different endpoints:
    
    | API             | Command                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
    |-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | Inference       | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>-d '{<br/>"model_name": "default",<br/>"model_version": "1.0",<br/>"id": "test_request",<br/>"inputs": [{<br/>"name": "input",<br/>"datatype": "INT32",<br/>"shape": [3],<br/>"contents": {"int_contents": [1,3,5]}<br/>}],<br/>"outputs": [{"name": "output"}]<br/>}' \\<br/>localhost:8080 inference.GrpcInferenceService/ModelInfer</pre> |
    | Model Metadata  | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>-d '{"name": "default", "version": "1.0"}' \\<br/>localhost:8080 inference.GrpcInferenceService/ModelMetadata</pre>                                                                                                                                                                                                                          |
    | Server Ready    | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>localhost:8080 inference.GrpcInferenceService/ServerReady</pre>                                                                                                                                                                                                                                                                              |
    | Server Live     | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>localhost:8080 inference.GrpcInferenceService/ServerLive</pre>                                                                                                                                                                                                                                                                               |
    | Server Metadata | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>localhost:8080 inference.GrpcInferenceService/ServerMetadata</pre>                                                                                                                                                                                                                                                                           |
    | Model Ready     | <pre>grpcurl -plaintext \\<br/>-import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \\<br/>-proto grpc_inference_service.proto \\<br/>-d '{"name": "default", "version": "1.0"}' \\<br/>localhost:8080 inference.GrpcInferenceService/ModelReady</pre>                                                                                                                                                                                                                             |
