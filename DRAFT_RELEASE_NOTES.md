# Major Additions

Major v1.5 refactoring in progress.

## New Features

### Core Library
- Implemented OIP-compliant request/response structures (`OipRequest`, `OipResponse`, `TensorData`)
- Added object detection support with `DefaultObjectDetectionTranslator`
- Created `ObjectDetectionBuilder` with fluent API for natural object detection inference
- Implemented `ObjectDetectionResult` value object with filtering and drawing capabilities
- Added image auto-encoding (PIL, numpy, file paths, bytes) in `DefaultObjectDetectionTranslator`
- Added `detect_object()` method to `InferenceClient` for easy object detection access
- Set up Behave BDD testing infrastructure with configuration and directory structure

### Modular Architecture
- Implemented `ModuleRegistry` for dynamic plugin discovery via Python entry points
- Added entry point groups: `oip.runtimes`, `oip.translators`, `oip.builders`
- Added `list_available_modules()`, `get_translator()`, `get_runtime()` methods to `InferenceClient`
- Core components now register via entry points for consistent discovery

### YOLO Module (`aissemble-oip-yolo`)
- Created new module for YOLO model family support
- Implemented `YOLORuntime` - MLServer-compatible runtime supporting YOLOv5, v8, v11
- Implemented `YOLOTranslator` extending `DefaultObjectDetectionTranslator`
- Module auto-registers via entry points when installed
- Supports model variant selection via `model-settings.json` parameters

### Object Detection Example
- Created working end-to-end example with real MLServer deployment
- Added Behave BDD tests that spin up MLServer automatically
- Tests verify full inference pipeline without mocking
- Example now uses `aissemble-oip-yolo` module instead of embedded runtime

## Architecture Improvements
- Model-specific code now isolated in separate modules under `aissemble-oip-modules/`
- Dependencies isolated per module (e.g., ultralytics only in yolo module)
- Modules can be versioned and released independently
- Clear pattern established for adding new model families
- Implemented `HttpOipAdapter` for HTTP communication with MLServer

# What's Changed
