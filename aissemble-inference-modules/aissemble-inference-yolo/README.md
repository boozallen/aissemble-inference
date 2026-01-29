# aiSSEMBLE OIP YOLO Module

YOLO model family support for the aiSSEMBLE Inference library.

## Supported Models

This module supports all YOLO versions available through the Ultralytics library:

| Family | Variants |
|--------|----------|
| YOLOv5 | yolov5n, yolov5s, yolov5m, yolov5l, yolov5x |
| YOLOv8 | yolov8n, yolov8s, yolov8m, yolov8l, yolov8x |
| YOLO11 | yolo11n, yolo11s, yolo11m, yolo11l, yolo11x |

## Installation

```bash
pip install aissemble-inference-yolo
```

This will also install the required dependencies:
- `aissemble-inference-core`
- `ultralytics` (for YOLO models)
- `mlserver` (for serving)

## Usage

### With MLServer

Create a `model-settings.json`:

```json
{
    "name": "yolo",
    "implementation": "aissemble_inference_yolo.YOLORuntime",
    "parameters": {
        "model": "yolov8n.pt"
    }
}
```

Start MLServer:

```bash
mlserver start /path/to/models
```

### With OIP Client

```python
from aissemble_inference_core.client import InferenceClient
from aissemble_inference_core.client.registry import ModuleRegistry

# The module auto-registers via entry points
print(ModuleRegistry.instance().list_available())
# {'runtimes': ['yolo'], 'translators': ['yolo'], ...}

# Use with InferenceClient
client = InferenceClient(adapter, endpoint)
result = client.detect_object("yolo").image("photo.jpg").run()
```

## Components

### YOLORuntime

MLServer-compatible runtime that wraps YOLO models:
- Accepts base64-encoded images via OIP protocol
- Returns bounding boxes, labels, and confidence scores
- Configurable model variant via parameters

### YOLOTranslator

Translator for YOLO outputs:
- Inherits from `DefaultObjectDetectionTranslator`
- Can be extended with YOLO-specific optimizations

## Entry Points

This module registers the following entry points:

| Group | Name | Class |
|-------|------|-------|
| `inference.runtimes` | yolo | `YOLORuntime` |
| `inference.translators` | yolo | `YOLOTranslator` |
