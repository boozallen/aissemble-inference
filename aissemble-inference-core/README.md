# aiSSEMBLE Inference (OIP) Client
Provides a modular Python library for standardized ML model inference, promoting interoperability across diverse 
runtimes and platforms. This client allows invocation of OIP endpoints in a more natural manner by ensuring that 
inference runtime details (like tensor-specific input/output structures) as not leaked from the model implementation
into the client.

## Features

### Fluent Builder API
InferenceBuilder (abstract base class) offers a task-specific, chainable interface for configuring inference requests.
Supports model selection, adapter/translator registration, custom parameters, and streaming responses.  Extensible via 
subclasses implementing `build_predictor()` to produce a Predictor instance.

### Task-Specific Inference
The client provides specialized builders for common ML tasks with natural, task-oriented APIs:

**Object Detection**
- `client.detect_object(model_name)` - Returns `ObjectDetectionBuilder`
- Fluent methods: `.image()`, `.confidence()`, `.labels()`
- Returns `ObjectDetectionResult` with bounding boxes, labels, scores
- Supports PIL images, numpy arrays, file paths, and bytes
- Example:
  ```python
  result = client.detect_object("yolov8") \
      .image("photo.jpg") \
      .confidence(0.6) \
      .run()
  for detection in result.detections:
      print(f"{detection.label}: {detection.confidence}")
  ```

**Text Summarization**
- `client.summarize(model_name)` - Returns `SummarizationBuilder`
- Fluent methods: `.text()`, `.max_length()`, `.min_length()`
- Returns `SummarizationResult` with summary text and compression metrics
- Example:
  ```python
  result = client.summarize("bart-large") \
      .text("Very long article text here...") \
      .max_length(100) \
      .run()
  print(result.summary)
  print(f"Compressed {result.compression_ratio:.1f}x")
  ```

### Raw Inference Support 
`RawInferenceBuilder` provides a low-level, non-fluent API for direct tensor inputs and parameters, ideal for custom or
performance-critical scenarios.

### Streaming Capable
Builders support iterable responses for continuous inference outputs.