# Major Additions

Major v1.5 refactoring in progress.

## New Features

### Core Library
- Implemented OIP-compliant request/response structures (`OipRequest`, `OipResponse`, `TensorData`)
- Added `HttpOipAdapter` for HTTP communication with OIP-compliant inference servers
- Set up Behave BDD testing infrastructure with configuration and directory structure

**Object Detection Support**
- Implemented `DefaultObjectDetectionTranslator` for OIP protocol conversion
- Created `ObjectDetectionBuilder` with fluent API for natural object detection inference
- Implemented `ObjectDetectionResult` value object with filtering and drawing capabilities
- Added image auto-encoding (PIL, numpy, file paths, bytes) in translator
- Added `detect_object()` method to `InferenceClient` for easy access

**Text Summarization Support**
- Implemented `DefaultSummarizationTranslator` for text-to-summary OIP protocol conversion
- Created `SummarizationBuilder` with fluent API (`.text()`, `.max_length()`, `.min_length()`)
- Implemented `SummarizationResult` value object with compression ratio calculation
- Added `summarize()` method to `InferenceClient` for easy access
- Supports configurable length constraints via OIP request parameters

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

### Sumy Module (`aissemble-oip-sumy`)
- Created new module for text summarization via the Sumy library
- Implemented `SumyRuntime` - MLServer-compatible runtime supporting multiple algorithms:
  - TextRank (graph-based ranking, default)
  - LSA (Latent Semantic Analysis)
  - LexRank (graph-based with cosine similarity)
- Implemented `SumyTranslator` extending `DefaultSummarizationTranslator`
- Module auto-registers via entry points when installed
- Configurable parameters: algorithm, sentences_count, language
- Multi-language support (English, Spanish, French, German, Italian, Portuguese, Russian, Czech, Slovak, etc.)
- Comprehensive test suite with unit and OIP integration tests
- Real MLServer integration tests replacing mock-based tests
- Test infrastructure with MLServer lifecycle management

### Object Detection Example
- Created working end-to-end example with real MLServer deployment
- Added Behave BDD tests that spin up MLServer automatically
- Tests verify full inference pipeline without mocking
- Example now uses `aissemble-oip-yolo` module instead of embedded runtime

### Summarization Example
- Created `aissemble-summarization-example` demonstrating text summarization end-to-end
- MLServer configurations for TextRank and LSA algorithms
- Comprehensive BDD test suite with 6 scenarios covering:
  - Multiple article lengths (short, medium, long)
  - Algorithm switching between TextRank and LSA
  - Parameter configuration validation
  - Error handling and edge cases
- Sample article test data for reproducible testing
- Full integration with InferenceClient fluent API
- README with comprehensive usage guide and troubleshooting

### Deploy Module (`aissemble-oip-deploy`) - Phase A
- Created new CLI module for generating deployment configurations
- **Key Value**: "Write once, deploy many" - generate version-controlled configs for any OIP model
- **Project Structure**: `aissemble-oip-deploy` is a **peer to aissemble-oip-core** (not under modules) because it's a framework that others extend
- **Extensibility**: Generators are discovered via Python entry points (`oip.generators`), allowing custom deployment targets (OpenShift, AWS SageMaker, air-gapped registries) to be added as separate packages
- CLI entry point: `oip deploy` command group
- Implemented generator framework:
  - `GeneratorRegistry` with entry point discovery for extensibility
  - Abstract `Generator` base class with model discovery and Jinja2 template rendering
  - `ModelInfo` dataclass for representing discovered models
  - Automatic detection of models from `model-settings.json` files
  - Public exports (`Generator`, `GeneratorRegistry`, `ModelInfo`) for custom generators
- Implemented `LocalGenerator` for local MLServer deployment:
  - Generates `run-mlserver.sh` startup script
  - Generates `README.md` with usage instructions
  - Auto-detects models and lists them in generated scripts
  - Registered via entry point for consistent discovery
- Configuration tracking via `.oip-deploy.yaml`:
  - Tracks generator version and generation timestamp
  - Records checksums of generated files (for future update/merge functionality)
  - Maintains list of active deployment targets
- CLI commands implemented:
  - `oip deploy init --target local` - generates local deployment configs
  - `oip deploy list-targets` - shows available generators with descriptions (discovered via entry points)
- Planned for future phases: Docker, Kubernetes, and KServe generators

## Architecture Improvements
- Model-specific code now isolated in separate modules under `aissemble-oip-modules/`
- Dependencies isolated per module (e.g., ultralytics only in yolo module, sumy only in sumy module)
- Modules can be versioned and released independently
- Clear pattern established for adding new model families
- `HttpOipAdapter` moved to core (from examples) for reusability across all OIP-compliant servers
- Established repeatable pattern for task-specific builders (object detection, summarization)
- Task-oriented API design isolates OIP protocol details in translators only

## Testing Improvements
- **Real MLServer integration tests** for aissemble-oip-sumy module
  - Replaced mock-based tests with actual OIP/HTTP communication
  - Tests now start real MLServer instances with configured models
  - Validates complete inference pipeline from HTTP request to response
  - Dynamic port allocation prevents test conflicts
  - Automatic cleanup after test scenarios
- **Reusable test infrastructure** pattern established
  - `environment.py` with MLServer lifecycle management
  - `start_mlserver_with_model()` helper for test setup
  - Temporary model configuration generation
  - Health check polling with retry logic
  - Consistent pattern across YOLO and Sumy modules
- **Integration test tagging** (`@integration`) for selective test execution
- **Sample test data** fixtures for reproducible results
- All tests passing with 100% success rate (18 scenarios for sumy, 6 for summarization example)

# What's Changed
