# aiSSEMBLE OIP Deploy

Deployment tooling for aiSSEMBLE Open Inference Protocol - generates deployment configurations for OIP-compatible models.

## Overview

`aissemble-oip-deploy` provides CLI tooling to generate deployment configurations for any OIP-compatible model. Users run a command, get version-controlled configs in their project, and can re-run to update while preserving customizations.

**Key Value**: Not just "possible to deploy" but "easy to deploy" - enterprise-ready, repeatable, version-controlled.

**Extensibility**: Generators are discovered via Python entry points, allowing custom deployment targets (OpenShift, AWS SageMaker, air-gapped registries) to be added as separate packages.

## Installation

```bash
pip install aissemble-oip-deploy
```

Or with uv:

```bash
uv add aissemble-oip-deploy
```

## Quick Start

Navigate to your project directory (containing a `models/` directory with your model configurations), then:

```bash
# Generate local deployment scripts
oip deploy init --target local

# Start MLServer locally
cd deploy/local && ./run-mlserver.sh
```

Or for containerized deployment:

```bash
# Generate Docker deployment configs
oip deploy init --target docker

# Build and run with Docker Compose
cd deploy/docker && docker-compose up --build
```

## CLI Reference

### `oip deploy init`

Initialize deployment configurations for your models.

```bash
oip deploy init [OPTIONS]
```

**Options:**
- `--target, -t` - Deployment target(s) to generate (default: local). Can be specified multiple times.
- `--model-dir, -m` - Path to models directory (default: ./models)
- `--output-dir, -o` - Output directory for generated configs (default: ./deploy)
- `--project-dir, -p` - Project root directory (default: current directory)

**Examples:**

```bash
# Generate local deployment only
oip deploy init --target local

# Generate Docker deployment
oip deploy init --target docker

# Generate multiple targets
oip deploy init --target local --target docker

# Generate for all available targets
oip deploy init --target all
```

### `oip deploy list-targets`

List available deployment targets. Generators are discovered via entry points.

```bash
oip deploy list-targets
```

## Built-in Generators

| Target | Description | Status |
|--------|-------------|--------|
| `local` | Local MLServer scripts for development | Available |
| `docker` | Containerized deployment with Docker Compose | Available |
| `kubernetes` | Standard K8s Deployment + Service | Coming soon |
| `kserve` | Serverless ML on Kubernetes | Coming soon |

## Generated Output Structure

After running `oip deploy init`, your project will have:

```
your-project/
  models/
    your-model/
      model-settings.json
  deploy/
    .oip-deploy.yaml          # Tracks generation metadata
    local/
      run-mlserver.sh         # Start MLServer locally
      README.md               # Local deployment instructions
    docker/
      Dockerfile              # Multi-stage build for MLServer
      docker-compose.yml      # Local container testing
      .dockerignore           # Build context exclusions
      README.md               # Docker deployment instructions
```

## Configuration Tracking

The `.oip-deploy.yaml` file tracks:
- Generator version used
- When configs were generated
- Which targets were generated
- Checksums of generated files (for future update/merge functionality)

## Creating Custom Generators

Custom generators can be added via the `oip.generators` entry point. This is useful for:
- Air-gapped environments with internal registries
- Platform-specific deployments (OpenShift, AWS SageMaker, etc.)
- Organization-specific deployment patterns

### Step 1: Create Your Generator

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

        generated_files = []
        target_dir = self.output_dir / "openshift"

        # Generate OpenShift-specific configs
        content = self.render_template(
            "openshift/deployment-config.yaml.j2",
            {"models": models, "registry": "my-internal-registry.example.com"}
        )
        path = self.write_file(target_dir / "deployment-config.yaml", content)
        generated_files.append(path)

        return generated_files
```

### Step 2: Register via Entry Point

```toml
# pyproject.toml
[project.entry-points."oip.generators"]
openshift = "my_org_deploy.openshift:OpenShiftGenerator"
```

### Step 3: Install and Use

```bash
pip install my-org-deploy
oip deploy list-targets  # Shows 'openshift' alongside built-in targets
oip deploy init --target openshift
```

## Development Status

This module is under active development. Currently implemented:
- [x] Phase A: Module skeleton + Local generator + Entry point discovery
- [x] Phase B: Docker generator with multi-stage Dockerfile + Docker Compose

Coming soon:
- [ ] Phase C: Kubernetes vanilla generator
- [ ] Phase D: KServe generator
- [ ] Phase E: Update/merge workflow
- [ ] Phase F: Example project + documentation

See [PLAN.md](./PLAN.md) for detailed implementation plan.

## License

Apache 2.0
