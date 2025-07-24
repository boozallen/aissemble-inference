[[Return to Main Documentation]](../README.md#examples)

# aiSSEMBLE Open Inference Protocol&trade; Examples
To see examples of how aiSSEMBLE Open Inference Protocol can be used, follow the links below.

## Examples

### FastAPI
- [Inference](./aissemble-oip-fastapi/aissemble-oip-fastapi-inference/README.md#aissemble-open-inference-protocol-fastapi-inference-example) - Implement custom inference logic and integrate it with the pre-configured REST endpoints provided by the framework.
- [Authorization](./aissemble-oip-fastapi/aissemble-oip-fastapi-auth/README.md#aissemble-open-inference-protocol-fastapi-authorization-example) - Add authorization to secure inference endpoints.

### gRPC
- [Inference](./aissemble-oip-grpc/aissemble-oip-grpc-inference/README.md#aissemble-open-inference-protocol-grpc-inference-example) - Implement custom handler for all Open Inference Protocol gRPC endpoints.
- [Authorization](./aissemble-oip-grpc/aissemble-oip-grpc-auth/README.md#aissemble-open-inference-protocol-grpc-authorization-example) - Use JWT-based authorization and role-based access control with a custom `AuthAdapter`.

### KServe
- [Inference](./aissemble-oip-kserve/aissemble-oip-kserve-inference/README.md#aissemble-open-inference-protocol-kserve-inference-example) - Implement custom handler with KServe.

### Shared
- [Content Type](./aissemble-oip-shared/README.md#content-type-decodingencoding) - Guide to using the `content_type` parameter for data handling in OIP-compliant requests, and defining custom codecs for advanced encoding and decoding.