# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

aiSSEMBLE Open Inference Protocol (OIP) is a modular, enterprise-ready Python library built on the Open Inference Protocol specification. The project is evolving into production-grade infrastructure for moving ML models from prototype to secure, scalable production deployment. It provides OIP-compliant client abstractions and is designed to integrate with MLServer, KServe, and other inference runtimes.

**Version**: 1.5.0-SNAPSHOT (Early Preview - Active Development)
**Python Version**: 3.11.4
**License**: Apache 2.0

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
│   │       ├── builder/               # Builder pattern implementations
│   │       │   ├── inference_builder.py      # Abstract base
│   │       │   └── raw_inference_builder.py  # Low-level API
│   │       ├── oip_adapter.py         # OIP protocol adapter
│   │       ├── translator.py          # Data format translator
│   │       └── predictor.py           # Prediction execution
│   ├── pyproject.toml
│   └── pom.xml
│
├── aissemble-oip-modules/       # Future extension modules (empty)
│
├── aissemble-oip-examples/      # Usage examples
│   └── aissemble-basic-mlserver-test/
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
- Core abstractions are in place but task-specific implementations are minimal
- The `aissemble-oip-modules` directory is a placeholder for future modules
- Examples use MLServer as the reference inference runtime
- All Python modules use Apache 2.0 license headers (managed by license-maven-plugin)
- Release notes should be updated in DRAFT_RELEASE_NOTES.md to ensure that they can be versioned

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
