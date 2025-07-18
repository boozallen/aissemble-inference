# aiSSEMBLE Open Inference Protocol gRPC Authorization Example

This example demonstrates how to implement JWT-based authorization for Open Inference Protocol gRPC endpoints role-based access using a custom `AuthAdapter`. The example shows how to create a secure gRPC server that requires valid JWT tokens for all inference requests.

## Authorization Flow

1. **Client Request**: Client sends gRPC request with JWT token in metadata
2. **Interceptor**: `AuthInterceptor` intercepts the request
3. **Token Validation**: JWT token is validated using secret and algorithm
4. **Authorization**: Optional authorization can be implemented through an adapter (example uses role-based authorization through custom `AuthAdapter`)
5. **Request Processing**: If valid, request is forwarded to the handler
6. **Response**: Handler response is returned to client

## Role-Based Access Control

This example uses a custom `AuthAdapter` that implements role-based access control:

- **admin**: Can access all endpoints (full permissions)
- **user**: Can access all endpoints except ModelInfer  
- **No role or unknown role**: Access denied to all endpoints

## Configuration

The example uses an `oip.properties` file to configure authorization:
- `auth_enabled`: Enable/disable authorization (default: false)
- `auth_secret`: Secret key for JWT validation (required if auth enabled)
- `auth_algorithm`: JWT algorithm (default: HS256)
- `protected_endpoints`: Comma-separated list of endpoints to protect (optional)
  - If `auth_enabled = true` and `protected_endpoints` is blank or not provided all endpoints will be protected.

**Important**: Make sure that your `auth_secret` and `auth_algorithm` in the `oip.properties` file matches the `AUTH_SECRET` and `AUTH_ALGORITHM` values in the `generate_jwt.py` file.

## Running the Example

### 1. Build and install dependencies to prepare the gRPC server by running the following Poetry command:
```sh
poetry install
```

### 2. Start the gRPC Server:

```bash
poetry run run_server
```

The server will start on `grpc://0.0.0.0:8080` with authorization enabled.

### 3. Generate JWT Tokens:

Generate test JWT tokens using the included utility:

```bash
poetry run generate_tokens
```

This will output tokens for different user types:
- Admin token (with "admin" role - full access)
- User token (with "user" role - access only to ServerReady)
- Basic token (access denied to all endpoints)

### 4. Test endpoint access:
- [grpcurl installation instructions](https://github.com/fullstorydev/grpcurl?tab=readme-ov-file#installation)
- `import-path` will need to be updated with the location of your `aissemble-open-inference-protocol` project

**Using grpcurl with Authorization**

Test without authorization (should fail):
```bash
grpcurl -plaintext \
  -import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \
  -proto grpc_inference_service.proto \
  localhost:8080 \
  inference.GrpcInferenceService/ServerReady
```

Test with authorization:
```bash
grpcurl -plaintext \
  -H "authorization: Bearer <YOUR_JWT_TOKEN_HERE>" \
  -import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \
  -proto grpc_inference_service.proto \
  localhost:8080 inference.GrpcInferenceService/ServerReady
```

### Test Model Inference with Authorization
This should pass with an admin token and fail with a user/basic token:
```bash
grpcurl -plaintext \
  -H "authorization: Bearer <YOUR_JWT_TOKEN_HERE>" \
  -import-path ../../../aissemble-open-inference-protocol-grpc/proto/ \
  -proto grpc_inference_service.proto \
  -d '{
    "model_name": "default",
    "model_version": "1.0",
    "id": "test_request",
    "inputs": [{
      "name": "input",
      "datatype": "FP32",
      "shape": [1],
      "contents": {"fp32_contents": [1.0]}
    }],
    "outputs": [{"name": "output"}]
  }' localhost:8080 inference.GrpcInferenceService/ModelInfer
```