# Tensor Abstraction in aiSSEMBLE OIP

This document demonstrates how aiSSEMBLE OIP abstracts tensor nuances from end users, allowing the same client code to work with different OIP server implementations that return vastly different tensor formats.

## The Problem: Tensor Leakage in Traditional OIP

Traditional OIP implementations force end users to deal with low-level tensor details:

```python
# ❌ Traditional OIP - User must handle raw tensors
response = requests.post("http://localhost:8080/v2/models/yolo/infer", json={
    "inputs": [{
        "name": "image",
        "shape": [1, 640, 640, 3],
        "datatype": "FP32",
        "data": [[...]]  # Raw tensor data
    }]
})

# User must manually parse response tensors
outputs = response.json()["outputs"]
bbox_tensor = next(o for o in outputs if o["name"] == "bboxes")
label_tensor = next(o for o in outputs if o["name"] == "labels")

# User must understand tensor shapes, data layouts, coordinate systems
bboxes = bbox_tensor["data"]  # Is this [N, 4] or [1, N, 4]? Pixel or normalized?
labels = label_tensor["data"]  # Strings or integers? Need mapping?

# User must manually create result objects
for bbox, label in zip(bboxes, labels):
    # What coordinate order? (x1,y1,x2,y2) or (ymin,xmin,ymax,xmax)?
    # Are these pixel coordinates or normalized [0,1]?
    # ...complexity leaks into application code
```

## The Solution: Translator Pattern

aiSSEMBLE OIP uses the **Translator pattern** to isolate all tensor complexity:

```python
# ✅ aiSSEMBLE OIP - User works with domain objects
from aissemble_inference_core.client import InferenceClient

client = InferenceClient(adapter=adapter, endpoint="http://localhost:8080")
result = (
    client.detect_object()
    .image("dog.jpg")
    .confidence(0.5)
    .run()
)

# Clean domain objects - no tensors in sight!
for detection in result.detections:
    print(f"{detection.label} at ({detection.bbox.x1}, {detection.bbox.y1}) "
          f"confidence: {detection.confidence:.2f}")
```

**The Translator handles ALL tensor complexity:**
- Tensor name mapping
- Shape transformations
- Data type conversions
- Coordinate system conversions
- Label encoding/decoding
- Batching/unbatching

## Demonstration: Two Different Tensor Formats

This example includes two translators that handle completely different tensor formats, yet present the **identical API** to end users.

### Format 1: Default (YOLO-style)

**Tensor Characteristics:**
- **Output tensors:** `bboxes`, `labels`, `scores`
- **Shape:** `[N, 4]` unbatched
- **Coordinates:** Pixel coordinates `(x1, y1, x2, y2)`
- **Labels:** String class names
- **Layout:** Separate tensors for each output type

**Example OIP Response:**
```json
{
  "outputs": [
    {
      "name": "bboxes",
      "shape": [3, 4],
      "datatype": "FP32",
      "data": [[100.0, 150.0, 300.0, 450.0],
               [50.0, 75.0, 200.0, 300.0],
               [400.0, 100.0, 600.0, 350.0]]
    },
    {
      "name": "labels",
      "shape": [3],
      "datatype": "BYTES",
      "data": ["dog", "cat", "person"]
    },
    {
      "name": "scores",
      "shape": [3],
      "datatype": "FP32",
      "data": [0.95, 0.87, 0.92]
    }
  ]
}
```

**Translator:** `DefaultObjectDetectionTranslator`

### Format 2: TensorFlow Object Detection API

**Tensor Characteristics:**
- **Output tensors:** `detection_boxes`, `detection_classes`, `detection_scores`, `num_detections`
- **Shape:** `[1, N, 4]` batched
- **Coordinates:** Normalized `[0, 1]` in order `(ymin, xmin, ymax, xmax)`
- **Labels:** Integer class IDs (require mapping to names)
- **Layout:** Batched outputs with explicit count

**Example OIP Response:**
```json
{
  "outputs": [
    {
      "name": "detection_boxes",
      "shape": [1, 3, 4],
      "datatype": "FP32",
      "data": [[[0.25, 0.16, 0.75, 0.50],
                [0.125, 0.08, 0.50, 0.33],
                [0.16, 0.66, 0.58, 1.0]]]
    },
    {
      "name": "detection_classes",
      "shape": [1, 3],
      "datatype": "INT32",
      "data": [[18, 17, 1]]
    },
    {
      "name": "detection_scores",
      "shape": [1, 3],
      "datatype": "FP32",
      "data": [[0.95, 0.87, 0.92]]
    },
    {
      "name": "num_detections",
      "shape": [1],
      "datatype": "INT32",
      "data": [3]
    }
  ]
}
```

**Translator:** `TensorFlowObjectDetectionTranslator`

### Key Differences Handled Transparently

| Aspect | Default Format | TensorFlow Format | User Impact |
|--------|---------------|-------------------|-------------|
| **Coordinate System** | Pixel coordinates | Normalized [0,1] | **None** - both return pixel coords in result |
| **Coordinate Order** | (x1, y1, x2, y2) | (ymin, xmin, ymax, xmax) | **None** - both return BoundingBox(x1, y1, x2, y2) |
| **Shape** | [N, 4] unbatched | [1, N, 4] batched | **None** - translator handles unbatching |
| **Label Format** | String names | Integer class IDs | **None** - translator maps IDs to names |
| **Tensor Names** | bboxes/labels/scores | detection_boxes/classes/scores | **None** - translator uses correct names |
| **Extra Metadata** | None | num_detections tensor | **None** - translator respects count |

## User Code Stays Identical

**With Default Translator:**
```python
from aissemble_inference_core.client import InferenceClient
from aissemble_inference_core.client.translators import DefaultObjectDetectionTranslator

client = InferenceClient(adapter=adapter, endpoint="http://localhost:8080")
result = (
    client.detect_object()
    .with_translator(DefaultObjectDetectionTranslator())
    .image("dog.jpg")
    .run()
)

for detection in result.detections:
    print(f"{detection.label}: {detection.confidence:.2f}")
```

**With TensorFlow Translator (different tensor format):**
```python
from aissemble_inference_core.client import InferenceClient
from aissemble_inference_core.client.translators import TensorFlowObjectDetectionTranslator

# Map COCO class IDs to names
coco_classes = {1: "person", 17: "cat", 18: "dog"}

client = InferenceClient(adapter=adapter, endpoint="http://localhost:8080")
result = (
    client.detect_object()
    .with_translator(TensorFlowObjectDetectionTranslator(class_names=coco_classes))
    .image("dog.jpg")  # Same image, different backend!
    .run()
)

# IDENTICAL result processing code!
for detection in result.detections:
    print(f"{detection.label}: {detection.confidence:.2f}")
```

**Output from both:** (Identical!)
```
dog: 0.95
cat: 0.87
person: 0.92
```

## Adding Support for New OIP Implementations

To integrate a new OIP server with different tensor formats:

1. **Implement a Translator** (only place that knows about tensors):

```python
from aissemble_inference_core.client.translator import Translator
from aissemble_inference_core.client.results import ObjectDetectionResult

class CustomServerTranslator(Translator[Any, ObjectDetectionResult]):
    def preprocess(self, input_data: Any) -> OipRequest:
        # Convert user input to whatever tensor format your server expects
        ...

    def postprocess(self, response: OipResponse) -> ObjectDetectionResult:
        # Parse your server's unique tensor format
        # Handle your coordinate systems, shapes, encodings, etc.
        # Return standard ObjectDetectionResult
        ...
```

2. **User code requires zero changes:**

```python
# Still the same API!
result = (
    client.detect_object()
    .with_translator(CustomServerTranslator())
    .image("dog.jpg")
    .run()
)
```

## Benefits of This Approach

1. **No Tensor Leakage**: Application code never sees tensors, shapes, or data types
2. **Pluggable Backends**: Swap OIP servers without changing user code
3. **Type Safety**: Users work with strongly-typed domain objects (`ObjectDetectionResult`, `BoundingBox`, `Detection`)
4. **Framework Agnostic**: Support MLServer, TensorFlow Serving, TorchServe, KServe, custom servers
5. **Testable**: Mock translators for testing without real inference servers
6. **Maintainable**: Tensor complexity isolated in one component
7. **Extensible**: Add new ML tasks by implementing new translators

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ User Application                                                 │
│                                                                  │
│  client.detect_object().image("dog.jpg").run()                 │
│         ↓                                                        │
│  ObjectDetectionResult { detections: [...] }                    │
└─────────────────────────────────────────────────────────────────┘
                              ↑
                    No tensors cross this boundary!
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Translator (Tensor Abstraction Layer)                           │
│                                                                  │
│  ┌──────────────────┐              ┌──────────────────┐        │
│  │ Default          │              │ TensorFlow       │        │
│  │ Translator       │              │ Translator       │        │
│  │                  │              │                  │        │
│  │ • [N, 4] shapes  │              │ • [1, N, 4]      │        │
│  │ • Pixel coords   │              │ • Normalized     │        │
│  │ • String labels  │              │ • Integer IDs    │        │
│  └──────────────────┘              └──────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    Raw OIP tensors only below here
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ OIP Server (MLServer, TensorFlow Serving, etc.)                │
│                                                                  │
│  Returns: Raw tensors in server-specific format                 │
└─────────────────────────────────────────────────────────────────┘
```

## Conclusion

The aiSSEMBLE OIP library's translator pattern provides complete abstraction of tensor complexity, allowing:

- **End users** to work with clean, typed domain objects
- **DevOps teams** to swap inference backends without code changes
- **ML engineers** to optimize tensor formats for performance
- **System integrators** to support heterogeneous OIP implementations

This architectural decision makes OIP truly enterprise-ready by hiding implementation details and providing a stable, framework-agnostic API.
