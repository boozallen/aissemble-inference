# Major Additions

Major v1.5 refactoring in progress.

## New Features
- Implemented OIP-compliant request/response structures (`OipRequest`, `OipResponse`, `TensorData`)
- Added object detection support with `DefaultObjectDetectionTranslator`
- Created `ObjectDetectionBuilder` with fluent API for natural object detection inference
- Implemented `ObjectDetectionResult` value object with filtering and drawing capabilities
- Added image auto-encoding (PIL, numpy, file paths, bytes) in `DefaultObjectDetectionTranslator`
- Added `detect_object()` method to `InferenceClient` for easy object detection access
- Set up Behave BDD testing infrastructure with configuration and directory structure

# What's Changed
