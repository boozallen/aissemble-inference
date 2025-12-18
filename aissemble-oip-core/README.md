# aiSSEMBLE Open Inference Protocol (OIP) Client
Provides a modular Python library for standardized ML model inference, promoting interoperability across diverse 
runtimes and platforms. This client allows invocation of OIP endpoints in a more natural manner by ensuring that 
inference runtime details (like tensor-specific input/output structures) as not leaked from the model implementation
into the client.

## Features

### Fluent Builder API
InferenceBuilder (abstract base class) offers a task-specific, chainable interface for configuring inference requests.
Supports model selection, adapter/translator registration, custom parameters, and streaming responses.  Extensible via 
subclasses implementing `build_predictor()` to produce a Predictor instance.

### Task Specific Inference (coming soon)

### Raw Inference Support 
`RawInferenceBuilder` provides a low-level, non-fluent API for direct tensor inputs and parameters, ideal for custom or
performance-critical scenarios.

### Streaming Capable
Builders support iterable responses for continuous inference outputs.