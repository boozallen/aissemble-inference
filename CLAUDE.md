# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

aiSSEMBLE Open Inference Protocol (OIP) is a modular, enterprise-ready Python library built on the Open Inference Protocol specification. The project is evolving into production-grade infrastructure for moving ML models from prototype to secure, scalable production deployment. It provides OIP-compliant client abstractions and is designed to integrate with MLServer, KServe, and other inference runtimes.

**Version**: 1.5.0-SNAPSHOT (Early Preview - Active Development)
**Python Version**: 3.11.4
**License**: Apache 2.0

### 🎯 Key Value Proposition: Tensor Abstraction

A major goal of this project is to **abstract tensor nuances from end users**. Traditional OIP implementations leak tensor details (shapes, data types, coordinate systems) into application code. aiSSEMBLE OIP uses the **Translator pattern** to completely isolate tensor complexity:

**Without aiSSEMBLE OIP (traditional approach):**
```python
# ❌ User must manually parse raw tensor responses
response = requests.post(url, json={"inputs": [...]})
outputs = response.json()["outputs"]
bbox_tensor = next(o for o in outputs if o["name"] == "bboxes")
# User must understand: Is this [N,4] or [1,N,4]? Pixel or normalized?
# What coordinate order? Need class ID mapping?
bboxes = bbox_tensor["data"]  # Tensor details leak into app code!
```

**With aiSSEMBLE OIP:**
```python
# ✅ User works with clean domain objects, zero tensor knowledge required
result = client.detect_object().image("dog.jpg").run()
for detection in result.detections:  # Strongly-typed domain objects
    print(f"{detection.label} at {detection.bbox}")
```

**Benefits:**
- Same user code works with different OIP backends (MLServer, TensorFlow Serving, KServe, custom)
- Translators handle all tensor complexity: shapes, coordinate systems, data layouts, label mappings
- Pluggable implementations without user code changes
- Type-safe domain objects instead of raw tensors

See `aissemble-oip-examples/aissemble-object-detection-example/TENSOR_ABSTRACTION.md` for detailed examples showing how multiple completely different tensor formats work with identical client code.

## Build System

This project uses a **hybrid Maven/Python build system** via the Habushu Maven plugin, which bridges Maven's lifecycle with Python's packaging tools (uv/Poetry).

### Common Build Commands

Build the entire project:
```bash
mvn clean install
```

Build with CI profile (for GitHub Actions):
```bash
mvn clean deploy -B -U -Pdefault-build,ci
```

Build for release (publishes to Maven Central and PyPI):
```bash
mvn clean deploy -Prelease
```

Build specific module (from root):
```bash
mvn clean install -pl aissemble-oip-core
```

### Python Development Commands

The project uses **uv** for Python dependency management. Each Python module has its own virtual environment managed by Habushu.

Navigate to a Python module (e.g., `aissemble-oip-core`) and use:

Activate virtual environment:
```bash
source .venv/bin/activate
```

Run linter (ruff):
```bash
ruff check .
```

Format code with ruff:
```bash
ruff format .
```

Install/sync dependencies:
```bash
uv sync
```

## Repository Structure

```
aissemble-open-inference-protocol/
├── aissemble-oip-core/          # Core OIP client library
│   ├── src/aissemble_oip_core/
│   │   └── client/              # Client abstractions
│   │       ├── inference_client.py    # Main facade
│   │       ├── registry.py            # Module discovery registry
│   │       ├── builder/               # Builder pattern implementations
│   │       │   ├── inference_builder.py      # Abstract base
│   │       │   ├── object_detection_builder.py  # Object detection
│   │       │   └── raw_inference_builder.py  # Low-level API
│   │       ├── translators/           # Data format translators
│   │       │   └── object_detection_translator.py
│   │       ├── results/               # Result value objects
│   │       │   └── object_detection_result.py
│   │       ├── oip_adapter.py         # OIP protocol adapter
│   │       ├── translator.py          # Translator base class
│   │       └── predictor.py           # Prediction execution
│   ├── pyproject.toml
│   └── pom.xml
│
├── aissemble-oip-deploy/        # Deployment config generation framework
│   ├── src/aissemble_oip_deploy/
│   │   ├── cli.py               # Click CLI (oip deploy)
│   │   ├── config.py            # .oip-deploy.yaml tracking
│   │   ├── registry.py          # Generator discovery via entry points
│   │   ├── generators/          # Built-in deployment target generators
│   │   │   ├── base.py          # Abstract Generator class
│   │   │   └── local.py         # Local MLServer generator
│   │   └── templates/           # Jinja2 templates
│   │       └── local/           # Local deployment templates
│   ├── README.md                # CLI + extensibility documentation
│   ├── PLAN.md                  # Implementation roadmap
│   ├── pyproject.toml           # With CLI + generator entry points
│   └── pom.xml
│
├── aissemble-oip-modules/       # Model-specific extension modules
│   ├── aissemble-oip-common-test/  # Reusable test utilities (build first!)
│   │   ├── src/aissemble_oip_common_test/
│   │   │   ├── mlserver_fixture.py     # MLServer lifecycle management
│   │   │   ├── behave_helpers.py       # Behave integration utilities
│   │   │   └── config_builder.py       # MLServer config generation
│   │   ├── README.md            # Usage guide with examples
│   │   ├── pyproject.toml       # Test-only dependencies
│   │   └── pom.xml              # Maven build config
│   │
│   ├── aissemble-oip-yolo/      # YOLO model family support
│   │   ├── src/aissemble_oip_yolo/
│   │   │   ├── runtime.py       # YOLORuntime (MLServer compatible)
│   │   │   └── translator.py    # YOLO-specific translator
│   │   ├── pyproject.toml       # With entry points registration
│   │   └── pom.xml
│   │
│   └── aissemble-oip-sumy/      # Text summarization support
│       ├── src/aissemble_oip_sumy/
│       │   ├── runtime.py       # SumyRuntime (TextRank, LSA, LexRank)
│       │   └── translator.py    # Sumy-specific translator
│       ├── tests/
│       │   ├── features/        # BDD tests with OIP integration
│       │   └── test-data/       # Sample articles for testing
│       ├── pyproject.toml       # With entry points registration
│       └── pom.xml
│
├── aissemble-oip-examples/      # Usage examples
│   ├── aissemble-object-detection-example/
│   │   ├── src/aissemble_object_detection_example/
│   │   │   └── http_adapter.py  # HTTP OipAdapter implementation
│   │   ├── models/              # MLServer model configurations
│   │   └── tests/features/      # Behave BDD tests
│   │
│   └── aissemble-summarization-example/
│       ├── models/              # MLServer configurations (TextRank, LSA)
│       │   ├── sumy-textrank/   # TextRank model config
│       │   └── sumy-lsa/        # LSA model config
│       ├── tests/
│       │   ├── test_data/       # Sample articles
│       │   └── features/        # Behave BDD tests
│       └── README.md            # Comprehensive usage guide
│
└── docs/design/                 # Architecture documentation
    └── client-design.md         # Client architecture details
```

## Architecture

The OIP client follows a layered architecture inspired by DJL (Deep Java Library):

### Client Architecture Layers

1. **InferenceClient** (Facade)
   - Entry point for all client operations
   - Zero-configuration construction
   - Provides task-specific factory methods (e.g., `detect_object()`, `summarize()`)
   - Location: `aissemble-oip-core/src/aissemble_oip_core/client/inference_client.py`

2. **InferenceBuilder** (Abstract Base)
   - Task-specific fluent API for configuring inference requests
   - Concrete implementations for each ML task (object detection, summarization, etc.)
   - Supports method chaining: `.with_model()`, `.with_adapter()`, `.with_translator()`, `.with_parameters()`
   - Streaming support via Python iterator protocol
   - Location: `aissemble-oip-core/src/aissemble_oip_core/client/builder/inference_builder.py`

3. **RawInferenceBuilder**
   - Low-level, non-fluent API for raw tensor inputs
   - Used only when task-specific abstractions are insufficient
   - Deliberately "ugly" to discourage accidental usage
   - Location: `aissemble-oip-core/src/aissemble_oip_core/client/builder/raw_inference_builder.py`

4. **Translator**
   - Only component aware of OIP JSON schema, tensor shapes, and protocol details
   - Pluggable and testable in isolation
   - Provides input preprocessing and output postprocessing
   - Location: `aissemble-oip-core/src/aissemble_oip_core/client/translator.py`

5. **Predictor**
   - Wraps a specific model endpoint
   - Manages resources (connection pools, retries, timeouts)
   - One instance per model reference for efficiency
   - StreamPredictor variant for streaming responses
   - Location: `aissemble-oip-core/src/aissemble_oip_core/client/predictor.py`

6. **OipAdapter**
   - Sole class interacting with OIP-compliant HTTP/gRPC endpoints
   - Stateless and mockable for testing
   - Implements backoff, authentication, metrics
   - Location: `aissemble-oip-core/src/aissemble_oip_core/client/oip_adapter.py`

### Design Philosophy

- **Hide runtime complexity**: Clients should not leak tensor/runtime details into application code
- **Task-oriented API**: Natural, task-specific methods instead of generic `predict()` calls
- **Fluent builder pattern**: Chainable configuration for readability
- **Extensibility**: New tasks added by subclassing `InferenceBuilder`
- **Protocol isolation**: Only `Translator` and `OipAdapter` know about OIP protocol details

See `docs/design/client-design.md` for class/sequence diagrams.

## Modular Architecture

The project uses a plugin-based modular architecture for model-specific implementations.

### Module Discovery

Modules register themselves via Python entry points, discovered automatically at runtime:

```python
from aissemble_oip_core.client import ModuleRegistry

registry = ModuleRegistry.instance()
print(registry.list_available())
# {'runtimes': ['yolo'], 'translators': ['yolo', 'object_detection'], 'builders': ['object_detection']}
```

### Entry Point Groups

- `oip.runtimes`: MLServer-compatible model runtimes
- `oip.translators`: OIP protocol translators
- `oip.builders`: Task-specific inference builders

### Creating a New Module

1. Create module under `aissemble-oip-modules/` (e.g., `aissemble-oip-resnet/`)
2. Implement runtime, translator, and/or builder classes
3. Register entry points in `pyproject.toml`:

```toml
[project.entry-points."oip.runtimes"]
resnet = "aissemble_oip_resnet:ResNetRuntime"

[project.entry-points."oip.translators"]
resnet = "aissemble_oip_resnet:ResNetTranslator"
```

4. Add module to `aissemble-oip-modules/pom.xml`
5. **Use `aissemble-oip-common-test` for MLServer test fixtures** (see Testing section below)

### Module Grouping Strategy

- **One module per model family** (not per version)
- Example: `aissemble-oip-yolo` supports YOLOv5, v8, v11 via configuration
- Version selection via parameters in `model-settings.json`
- Split into separate modules only when:
  - Different underlying frameworks required
  - Incompatible dependency versions
  - Vastly different output formats

## Maven Profiles

- **default-build**: Standard build, deploys snapshots to GitHub Packages
- **ci**: GitHub Actions profile with specific Habushu configurations (delete venv, force sync, etc.)
- **release**: Production release profile targeting Maven Central and PyPI

## Python Package Management

The project uses **Habushu** (Maven plugin) which wraps **uv** for Python dependency management. Dependencies are specified in `pyproject.toml` files and locked in `uv.lock` files.

### Key Habushu Configuration Properties

- `pythonVersion`: 3.11.4 (controlled in root `pom.xml`)
- `cacheWheels`: true (caches Python wheels for faster builds)
- `skipDeploy`: true for examples/modules (they don't publish to PyPI)

## Minimalist Implementation Rule

- Always implement the absolute minimum to meet the specified task requirements.
- When in doubt about scope, choose the narrower interpretation.
- Keep functions small - preferrably under 100 line
- Write concise, technical Python code with accurate examples
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError)
- Implement proper error handling

## Development Workflow

1. Make changes to Python code in `aissemble-oip-core/src/`
2. Run linter: `cd aissemble-oip-core && ruff check .`
3. Build module: `mvn clean install -pl aissemble-oip-core` (from root)
4. Test changes manually or with examples in `aissemble-oip-examples/`

## Git Workflow

- **Main branch**: `dev` (not `main`)
- Create feature branches from `dev`
- PRs should target `dev`
- CI runs on pushes to `dev` and on pull requests

## Important Notes

- The project is in **early preview** (v1.5) - not feature-complete
- Many TODOs exist in the codebase indicating planned functionality
- Core abstractions are in place with object detection as the reference implementation
- The `aissemble-oip-modules` directory contains model-specific modules (e.g., `aissemble-oip-yolo`)
- New model families should be added as modules, not embedded in examples
- Modules auto-register via Python entry points for dynamic discovery
- Examples use MLServer as the reference inference runtime
- All Python modules use Apache 2.0 license headers (managed by license-maven-plugin)
- Release notes should be updated in DRAFT_RELEASE_NOTES.md to ensure that they can be versioned
- No need to add licenses to files or projects - the Maven build will handle this for us

## CI/CD

GitHub Actions workflow: `.github/workflows/build.yaml`

- Runs daily at 6am UTC
- Runs on pushes to `dev` branch
- Manual trigger via workflow_dispatch
- Uses custom action: `.github/actions/install_dependencies`
- Requires secrets for:
  - SONATYPE_CENTRAL_REPO_TOKEN_USER/KEY (Maven Central)
  - TEST_PYPI_USERNAME/TOKEN (PyPI publishing)
  - GITHUB_TOKEN (GitHub Packages)

## Testing

Behave is the preferred testing framework for BDD-style tests.

### Running Tests

From `aissemble-oip-core`:

```bash
# Install test dependencies
uv sync --group test

# Run all behave tests
behave

# Run specific feature
behave tests/features/your_feature.feature

# Run with tags
behave --tags=@smoke
```

### Test Structure

```
aissemble-oip-core/tests/
├── features/              # Behave .feature files
│   ├── steps/            # Step definitions
│   ├── environment.py    # Test hooks
│   └── .gitkeep
├── test_data/            # Test fixtures
└── README.md
```

Configuration is in `aissemble-oip-core/behave.ini`.

See `aissemble-oip-core/tests/README.md` for detailed testing documentation.

### Common Test Utilities (aissemble-oip-common-test)

The `aissemble-oip-common-test` module provides reusable MLServer test infrastructure to avoid code duplication across modules and examples.

**Key Features:**
- **MLServerFixture**: Context manager for MLServer lifecycle (start, stop, cleanup)
- **Behave helpers**: Drop-in functions for `environment.py` hooks
- **Config builders**: JSON generation for MLServer settings

**Usage in new modules/examples:**

Add to `pyproject.toml`:
```toml
[dependency-groups]
test = [
    "behave>=1.2.6",
    "mlserver>=1.6.0",
    "aissemble-oip-common-test",
]

[tool.uv.sources]
aissemble-oip-common-test = { path = "../aissemble-oip-common-test", editable = true }
```

**For static model directories (examples):**
```python
# tests/features/environment.py
from pathlib import Path
from aissemble_oip_common_test.behave_helpers import (
    setup_mlserver_simple,
    teardown_mlserver,
)

def before_all(context):
    models_dir = Path(__file__).parent.parent.parent / "models"
    setup_mlserver_simple(context, models_dir=models_dir, port=8080)
    context.mlserver_fixture.start()

def after_all(context):
    teardown_mlserver(context)
```

**For dynamic config generation (module tests):**
```python
# tests/features/environment.py
from aissemble_oip_common_test.behave_helpers import (
    setup_mlserver_dynamic,
    teardown_mlserver,
    start_mlserver_with_model,
)

def before_all(context):
    setup_mlserver_dynamic(context)

def after_scenario(context, scenario):
    if hasattr(context, "mlserver_fixture") and context.mlserver_fixture.process:
        context.mlserver_fixture.stop()

def after_all(context):
    teardown_mlserver(context)

# In step definitions:
start_mlserver_with_model(
    context,
    model_name="your-model",
    runtime="your_module.YourRuntime",
    param1="value1"
)
```

**Important Notes:**
- `aissemble-oip-common-test` must be built **first** (it's listed first in `aissemble-oip-modules/pom.xml`)
- Uses context manager protocol (`__enter__`/`__exit__`) for automatic cleanup
- Supports both fixed ports (examples) and dynamic port allocation (module tests)
- Logs warnings for cleanup failures instead of silent errors

See `aissemble-oip-modules/aissemble-oip-common-test/README.md` for complete API documentation.

### Deployment Tooling (aissemble-oip-deploy)

The `aissemble-oip-deploy` module is a **peer to aissemble-oip-core** that provides CLI tooling to generate deployment configurations for any OIP-compatible model. The goal is "write once, deploy many" - users get version-controlled configs in their project.

**Generators are discovered via entry points**, allowing custom deployment targets (OpenShift, AWS SageMaker, air-gapped registries) to be added as separate packages without modifying the core deploy module.

**CLI Commands:**
```bash
# Generate local deployment scripts
oip deploy init --target local

# List available targets (discovers generators via entry points)
oip deploy list-targets
```

**Architecture:**
- `cli.py` - Click-based CLI with `oip deploy` command group
- `registry.py` - Generator discovery via `oip.generators` entry point group
- `config.py` - Manages `.oip-deploy.yaml` tracking file (versions, checksums)
- `generators/base.py` - Abstract `Generator` class with model discovery and template rendering
- `generators/local.py` - Local MLServer generator (registered via entry point)
- `templates/` - Jinja2 templates for each deployment target

**Adding a Custom Generator (External Package):**

Custom generators can be added without modifying aissemble-oip-deploy:

1. Create your generator package:
```python
# my_org_deploy/openshift.py
from aissemble_oip_deploy import Generator, ModelInfo
from pathlib import Path

class OpenShiftGenerator(Generator):
    """Generator for OpenShift deployments."""
    name = "openshift"

    def generate(self, models: list[ModelInfo] | None = None) -> list[Path]:
        if models is None:
            models = self.detect_models()
        # Generate files using self.render_template() and self.write_file()
        return generated_files
```

2. Register via entry point in `pyproject.toml`:
```toml
[project.entry-points."oip.generators"]
openshift = "my_org_deploy.openshift:OpenShiftGenerator"
```

3. Install and use:
```bash
pip install my-org-deploy
oip deploy list-targets  # Shows 'openshift' alongside built-in targets
oip deploy init --target openshift
```

**Development Status:**
- Phase A (complete): Module skeleton + Local generator + Entry point discovery
- Phase B-D (planned): Docker, Kubernetes, KServe generators
- Phase E (planned): Update/merge workflow with conflict detection
- Phase F (planned): Example project + documentation

See `aissemble-oip-deploy/README.md` for full documentation.
