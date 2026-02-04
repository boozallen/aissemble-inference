# aiSSEMBLE&trade; Inference

![PyPI - Version](https://img.shields.io/pypi/v/aissemble-inference-core)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aissemble-inference-core)
![PyPI - Format](https://img.shields.io/pypi/format/aissemble-inference-core)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aissemble-inference-core)
[![Build (github)](https://github.com/boozallen/aissemble-open-inference-protocol/actions/workflows/build.yaml/badge.svg)](https://github.com/boozallen/aissemble-open-inference-protocol/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/boozallen/aissemble-open-inference-protocol)](https://www.apache.org/licenses/LICENSE-2.0)

A modular Python library for deploying ML models to production using the [Open Inference Protocol](https://github.com/kserve/open-inference-protocol). Built on MLServer, designed for enterprise deployment.

## How aiSSEMBLE Inference Fits In

aiSSEMBLE Inference is a **toolkit for the full ML deployment lifecycle** - from packaging models to consuming them in applications. It leverages [MLServer](https://mlserver.readthedocs.io/) as the inference runtime across all environments, with optional [KServe](https://kserve.github.io/) integration for serverless Kubernetes deployments.

```
┌─────────────────────────────────────────────────────────────────┐
│                     aiSSEMBLE Inference                         │
│    Deployment Tooling (inference deploy)  +  Client Library     │
└──────────────────────────────┬──────────────────────────────────┘
                               │ generates / speaks OIP to
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                          MLServer                               │
│    Lightweight Python inference server - works everywhere       │
│    Local  →  Docker  →  Kubernetes  →  KServe (optional)        │
└─────────────────────────────────────────────────────────────────┘
```

### What aiSSEMBLE Inference Adds

| Layer | What It Does |
|-------|--------------|
| **`inference deploy`** | Generates deployment configs for MLServer across environments |
| **Client library** | Abstracts tensor complexity into task-specific APIs |

### Deployment Progression

| Target | Infrastructure | Use Case |
|--------|---------------|----------|
| `local` | MLServer | Development |
| `docker` | MLServer + Docker | Containerized deployment |
| `kubernetes` | MLServer + K8s | Production Kubernetes |
| `kserve` | MLServer + KServe | Serverless ML (autoscaling, scale-to-zero) |

**You don't need aiSSEMBLE Inference if** you already have deployment workflows and OIP client code you're happy with - MLServer and KServe are excellent tools on their own.

## Key Features

### Tensor Abstraction

Work with domain objects, not raw tensors:

```python
# Traditional OIP: Manual tensor parsing
outputs = response.json()["outputs"]
bbox_tensor = next(o for o in outputs if o["name"] == "bboxes")
bboxes = bbox_tensor["data"]  # Is this [N,4] or [1,N,4]? What coordinate system?

# aiSSEMBLE Inference: Typed domain objects
client = InferenceClient(adapter, endpoint)
result = client.detect_object().image("dog.jpg").confidence(0.5).run()
for detection in result.detections:
    print(f"{detection.label} at {detection.bbox}")
```

### Write Once, Deploy Many

Generate deployment configs for multiple targets from a single model:

```bash
pip install aissemble-inference-deploy
inference deploy init --target local --target docker --target kubernetes --target kserve
```

| Target | Description |
|--------|-------------|
| `local` | MLServer scripts for development |
| `docker` | Multi-stage Dockerfile + Docker Compose |
| `kubernetes` | Kustomize manifests with dev/prod overlays |
| `kserve` | ServingRuntime + InferenceService with scale-to-zero |

See [`aissemble-inference-deploy/README.md`](./aissemble-inference-deploy/README.md) for details.

## Installation

```bash
# Core library
pip install aissemble-inference-core

# Model modules (install as needed)
pip install aissemble-inference-yolo    # YOLO object detection
pip install aissemble-inference-sumy    # Text summarization

# Deployment tooling
pip install aissemble-inference-deploy
```

## Modules

| Module | Description |
|--------|-------------|
| `aissemble-inference-core` | Base abstractions (OipAdapter, Translator, Predictor) |
| `aissemble-inference-deploy` | Deployment config generation (Local, Docker, K8s, KServe) |
| `aissemble-inference-yolo` | YOLO model family (v5, v8, v11) |
| `aissemble-inference-sumy` | Text summarization (TextRank, LSA, LexRank) |

Modules auto-register via Python entry points:

```python
from aissemble_inference_core.client import InferenceClient, ModuleRegistry

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

- **Object Detection**: [`aissemble-inference-examples/aissemble-object-detection-example/`](./aissemble-inference-examples/aissemble-object-detection-example/)
- **Text Summarization**: [`aissemble-inference-examples/aissemble-summarization-example/`](./aissemble-inference-examples/aissemble-summarization-example/)

## License

Apache 2.0
