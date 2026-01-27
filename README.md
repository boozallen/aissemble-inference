# aiSSEMBLE&trade; Open Inference Protocol

![PyPI - Version](https://img.shields.io/pypi/v/aissemble-oip-core)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aissemble-oip-core)
![PyPI - Format](https://img.shields.io/pypi/format/aissemble-oip-core)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aissemble-oip-core)
[![Build (github)](https://github.com/boozallen/aissemble-open-inference-protocol/actions/workflows/build.yaml/badge.svg)](https://github.com/boozallen/aissemble-open-inference-protocol/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/boozallen/aissemble-open-inference-protocol)](https://www.apache.org/licenses/LICENSE-2.0)

A modular Python library for deploying ML models to production using the [Open Inference Protocol](https://github.com/kserve/open-inference-protocol). Built on MLServer, designed for enterprise deployment.

## Key Features

### Tensor Abstraction

Work with domain objects, not raw tensors:

```python
# Traditional OIP: Manual tensor parsing
outputs = response.json()["outputs"]
bbox_tensor = next(o for o in outputs if o["name"] == "bboxes")
bboxes = bbox_tensor["data"]  # Is this [N,4] or [1,N,4]? What coordinate system?

# aiSSEMBLE OIP: Typed domain objects
client = InferenceClient(adapter, endpoint)
result = client.detect_object().image("dog.jpg").confidence(0.5).run()
for detection in result.detections:
    print(f"{detection.label} at {detection.bbox}")
```

### Write Once, Deploy Many

Generate deployment configs for multiple targets from a single model:

```bash
pip install aissemble-oip-deploy
oip deploy init --target local --target docker --target kubernetes --target kserve
```

| Target | Description |
|--------|-------------|
| `local` | MLServer scripts for development |
| `docker` | Multi-stage Dockerfile + Docker Compose |
| `kubernetes` | Kustomize manifests with dev/prod overlays |
| `kserve` | ServingRuntime + InferenceService with scale-to-zero |

See [`aissemble-oip-deploy/README.md`](./aissemble-oip-deploy/README.md) for details.

## Installation

```bash
# Core library
pip install aissemble-oip-core

# Model modules (install as needed)
pip install aissemble-oip-yolo    # YOLO object detection
pip install aissemble-oip-sumy    # Text summarization

# Deployment tooling
pip install aissemble-oip-deploy
```

## Modules

| Module | Description |
|--------|-------------|
| `aissemble-oip-core` | Base abstractions (OipAdapter, Translator, Predictor) |
| `aissemble-oip-deploy` | Deployment config generation (Local, Docker, K8s, KServe) |
| `aissemble-oip-yolo` | YOLO model family (v5, v8, v11) |
| `aissemble-oip-sumy` | Text summarization (TextRank, LSA, LexRank) |

Modules auto-register via Python entry points:

```python
from aissemble_oip_core.client import InferenceClient, ModuleRegistry

# Discover installed modules
print(ModuleRegistry.instance().list_available())
# {'runtimes': ['yolo', 'sumy'], 'translators': ['yolo', 'sumy', 'object_detection'], ...}

# Use object detection with fluent API
client = InferenceClient(adapter, endpoint)
result = client.detect_object("yolo").image("photo.jpg").confidence(0.5).run()

# Text summarization
summary = client.summarize("sumy").text("Long article...").max_length(100).run()
```

## Examples

- **Object Detection**: [`aissemble-oip-examples/aissemble-object-detection-example/`](./aissemble-oip-examples/aissemble-object-detection-example/)
- **Text Summarization**: [`aissemble-oip-examples/aissemble-summarization-example/`](./aissemble-oip-examples/aissemble-summarization-example/)

## License

Apache 2.0
