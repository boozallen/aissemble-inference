# aiSSEMBLE Object Detection Example

A working example demonstrating object detection using the aiSSEMBLE Open Inference Protocol (OIP) library with a real MLServer deployment and YOLOv8 model.

## Overview

This example shows how to:

1. Create an HTTP adapter for OIP communication
2. Use the `aissemble-oip-yolo` module for YOLO model support
3. Use the OIP client's fluent API for object detection
4. Run end-to-end tests that spin up MLServer automatically
5. Leverage the module registry for dynamic module discovery
6. **Demonstrate tensor abstraction** - how the library hides tensor complexity from end users

> **Note:** For an overview of tensor abstraction in aiSSEMBLE OIP, see the [main project README](../../README.md#-key-value-proposition-tensor-abstraction). For detailed technical examples showing two different tensor formats with identical user code, see [TENSOR_ABSTRACTION.md](./TENSOR_ABSTRACTION.md).

## Project Structure

```
aissemble-object-detection-example/
├── src/aissemble_object_detection_example/
│   ├── __init__.py
│   └── http_adapter.py          # HTTP OipAdapter implementation
├── models/yolov8/
│   └── model-settings.json      # MLServer model configuration
├── tests/
│   └── features/
│       ├── object_detection.feature
│       ├── environment.py       # MLServer startup/shutdown
│       └── steps/
│           └── object_detection_steps.py
├── pyproject.toml
├── behave.ini
└── README.md
```

Note: The YOLORuntime is provided by the `aissemble-oip-yolo` module, not embedded in this example.

## Prerequisites

- Python 3.11+
- uv (for dependency management)

## Installation

From this directory:

```bash
# Install dependencies including test dependencies
uv sync --group test
```

This will install:
- `aissemble-oip-core` (from local source)
- `aissemble-oip-yolo` (YOLO module with runtime)
- `mlserver` (inference server)
- `ultralytics` (YOLOv8, via aissemble-oip-yolo)
- `behave` (BDD testing framework)

## Running the Tests

The tests automatically start MLServer, load the YOLOv8 model, run inference, and verify results:

```bash
# Run all tests
uv run behave

# Run with verbose output
uv run behave -v

# Run specific scenario
uv run behave --name "Detect objects"
```

## Usage Example

```python
from aissemble_oip_core.client.inference_client import InferenceClient
from aissemble_oip_core.client.oip_adapter import HttpOipAdapter

# Create adapter pointing to MLServer
adapter = HttpOipAdapter(
    base_url="http://localhost:8080",
    model_name="yolov8"
)

# Create client and run detection
client = InferenceClient(adapter=adapter, endpoint="http://localhost:8080")
result = (
    client.detect_object()
    .image("path/to/image.jpg")
    .confidence(0.5)
    .run()
)

# Process results
for detection in result.detections:
    print(f"Found {detection.label} at {detection.bbox} "
          f"with confidence {detection.confidence:.2f}")
```

## Running MLServer Manually

To start MLServer manually for development:

```bash
cd aissemble-object-detection-example
uv run mlserver start models
```

Then test with curl:

```bash
curl -X POST http://localhost:8080/v2/models/yolov8/infer \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [{
      "name": "image",
      "shape": [1, -1],
      "datatype": "BYTES",
      "data": [["<base64-encoded-image>"]]
    }]
  }'
```

## Components

### HttpOipAdapter

A concrete implementation of `OipAdapter` that communicates with MLServer over HTTP:

```python
from aissemble_oip_core.client.oip_adapter import HttpOipAdapter

adapter = HttpOipAdapter(
    base_url="http://localhost:8080",
    model_name="yolov8",
    timeout=30.0
)
```

### YOLORuntime (from aissemble-oip-yolo)

The `aissemble-oip-yolo` module provides the `YOLORuntime` class that:

- Supports multiple YOLO versions (v5, v8, v11) via Ultralytics
- Loads the configured model variant on startup
- Accepts base64-encoded images in OIP format
- Returns detections with bounding boxes, labels, and confidence scores
- Auto-registers via entry points for module discovery

### Test Features

The Behave tests (`tests/features/object_detection.feature`) verify:

- End-to-end object detection pipeline
- Confidence threshold filtering
- Response structure validation

## Notes

- The default test creates a synthetic image with geometric shapes. YOLOv8 is trained on COCO dataset objects (people, cars, animals, etc.), so it may not detect shapes in the synthetic image. This still validates the pipeline works end-to-end.
- For better detection results, place real photographs in `tests/test_data/` and update the step definitions.
- First run may be slow as YOLOv8 downloads the model weights (~6MB for yolov8n).
- The `models/settings.json` disables MLServer's parallel workers to avoid compatibility issues with uvloop on Python 3.12.
