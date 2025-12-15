# aiSSEMBLE Open Inference Protocol - MLServer Object Detection Example

This example demonstrates how to use MLServer with the Open Inference Protocol for object detection using the YOLO-based `hustvl/yolos-small` model from HuggingFace.

## Overview

The example implements:
- Custom MLServer model (`ImgDetection`) that inherits from `MLModel`
- Object detection on base64-encoded images
- Inference endpoints compliant with the Open Inference Protocol v2

## Prerequisites

- Python 3.11.4+
- uv

## Local Development

### 1. Install Dependencies
```bash
uv sync
```
### 2. Start server
```bash
uv run python src/object_detection/server.py
```
the server will start and explose the following ports:
The server will start and expose the following ports:
- 8080: HTTP/REST API
- 8081: gRPC API
- 8082: Prometheus metrics

### 3. Test with an Image

Use the provided client script to test object detection:

```bash
uv run python client.py /path/to/image.jpg
```

## API Endpoints
Inference
- POST http://localhost:8080/v2/models/img-detection/infer 
    - Run object detection inference
Health Checks
- GET http://localhost:8080/v2/health/live 
    - Liveness check
- GET http://localhost:8080/v2/health/ready 
    - Readiness check
Metadata
- GET http://localhost:8080/v2/models/img-detection 
    - Model metadata
- GET http://localhost:8082/metrics 
    - Prometheus metrics

### Example Usage
#### Check if server is ready
curl -v http://localhost:8080/v2/health/ready

#### View model metadata
curl http://localhost:8080/v2/models/img-detection

#### View metrics
curl http://localhost:8082/metrics