[[Return to Main Documentation]](../README.md#examples)

# aiSSEMBLE&trade; Open Inference Protocol Examples
To see examples of how aiSSEMBLE Open Inference Protocol can be used, follow the links below.

## Examples

### FastAPI
- [Getting started](./aissemble-oip-fastapi/aissemble-oip-fastapi-inference/README.md#aissemble-open-inference-protocol-fastapi-getting-started-example) - Implement model inference logic and integrate it with the pre-configured REST endpoints provided by the framework.
- [Authorization](./aissemble-oip-fastapi/aissemble-oip-fastapi-auth/README.md#aissemble-open-inference-protocol-fastapi-authorization-example) - Add authorization to secure inference endpoints.

### gRPC
- [Getting started](./aissemble-oip-grpc/aissemble-oip-grpc-inference/README.md#aissemble-open-inference-protocol-grpc-getting-started-example) - Implement model inference logic and integrate it with the pre-configured gRPC endpoints provided by the framework.
- [Authorization](./aissemble-oip-grpc/aissemble-oip-grpc-auth/README.md#aissemble-open-inference-protocol-grpc-authorization-example) - Use JWT-based authorization and role-based access control with a custom `AuthAdapter`.

### KServe
- [Getting started](./aissemble-oip-kserve/aissemble-oip-kserve-inference/README.md#aissemble-open-inference-protocol-kserve-getting-started-example) - Leverage implemented model inference logic with KServe.
- [Containerization](./aissemble-oip-kserve/aissemble-oip-kserve-containerization/README.md) - Guide to containerize Open Inference Protocol and deploy it on KServe

### Shared
- [Content Type](./aissemble-oip-shared/README.md#content-type-decodingencoding) - Guide to using the `content_type` parameter for data handling in OIP-compliant requests, and defining custom codecs for advanced encoding and decoding.
