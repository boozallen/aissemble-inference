# aiSSEMBLE&trade; Open Inference Protocol

![PyPI - Version](https://img.shields.io/pypi/v/aissemble-open-inference-protocol-shared)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aissemble-open-inference-protocol-shared)
![PyPI - Format](https://img.shields.io/pypi/format/aissemble-open-inference-protocol-shared)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aissemble-open-inference-protocol-shared)
[![Build (github)](https://github.com/boozallen/aissemble-open-inference-protocol/actions/workflows/build.yaml/badge.svg)](https://github.com/boozallen/aissemble-open-inference-protocol/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/boozallen/aissemble-open-inference-protocol)](https://www.apache.org/licenses/LICENSE-2.0)

**v1.5 – Early Preview**

The aiSSEMBLE [Open Inference Protocol (OIP)](https://github.com/kserve/open-inference-protocol) project is evolving 
from a reference implementation of the Open Inference Protocol into a **modular, enterprise-ready Python library** 
designed to help data science teams move ML models from prototype to secure, scalable production with minimal friction.

## High-Level Goals for v1.5

- Remain fully compliant with the Open Inference Protocol (OIP) specification  
- Provide a lightweight, extensible library built on MLServer as the core inference engine  
- Serve as production-grade “glue” between existing data science artifacts and enterprise deployment targets  
- Enable rapid, repeatable deployment to diverse environments (Kubernetes, AWS, on-prem, edge)  
- Offer pluggable integrations and sensible defaults for:  
  - Security (authentication, authorization, encryption)  
  - Observability (centralized logging, Prometheus/Grafana metrics)  
  - Compliance needs common in regulated settings (FedRAMP, NIST, DoD IL support)  
- Simplify handoffs across data scientists, software engineers, and DevSecOps teams via standardized, framework-agnostic 
 abstractions  

This version focuses on establishing the core architecture, extension points, and initial capabilities. Detailed
documentation, examples, contribution guides, and full feature specifications will be expanded progressively as part
of the v1.5 effort.

## Modular Architecture

The library uses a plugin-based architecture for model-specific implementations:

```
aissemble-oip-core          # Base abstractions (OipAdapter, Translator, Predictor)
aissemble-oip-yolo          # YOLO model family (YOLOv5, v8, v11)
aissemble-oip-sumy          # Text summarization (TextRank, LSA, LexRank)
aissemble-oip-<model>       # Future: ResNet, Whisper, LLaMA, etc.
```

Modules auto-register via Python entry points:

```python
from aissemble_oip_core.client import InferenceClient, ModuleRegistry

# Discover installed modules
print(ModuleRegistry.instance().list_available())
# {'runtimes': ['yolo', 'sumy'], 'translators': ['yolo', 'sumy', 'object_detection'], ...}

# Use object detection with fluent API
client = InferenceClient(adapter, endpoint)
result = client.detect_object("yolo").image("photo.jpg").confidence(0.5).run()

# Use text summarization
summary = client.summarize("bart-large").text("Long article...").max_length(100).run()
print(summary.summary)
```

## Quick Start

```bash
# Install core library with model modules
pip install aissemble-oip-core aissemble-oip-yolo aissemble-oip-sumy

# Or install from source
cd aissemble-oip-core && uv sync
cd ../aissemble-oip-modules/aissemble-oip-yolo && uv sync
cd ../aissemble-oip-sumy && uv sync
```

### Examples

Complete working examples demonstrating end-to-end usage:

- **Object Detection**: `aissemble-oip-examples/aissemble-object-detection-example/`
  - YOLO model integration with MLServer
  - Image-based inference workflows
  - BDD testing patterns

- **Text Summarization**: `aissemble-oip-examples/aissemble-summarization-example/`
  - Sumy integration with multiple algorithms (TextRank, LSA, LexRank)
  - Text-based inference workflows
  - MLServer configuration examples

**Status:** Active development – not yet feature-complete.
Feedback and early adopters welcome.