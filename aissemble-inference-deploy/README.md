# aiSSEMBLE Inference Deploy

Deployment tooling for aiSSEMBLE Inference - generates deployment configurations for OIP-compatible models.

## Overview

`aissemble-inference-deploy` provides CLI tooling to generate deployment configurations for any OIP-compatible model. Users run a command, get version-controlled configs in their project, and can re-run to update while preserving customizations.

**Key Value**: Not just "possible to deploy" but "easy to deploy" - enterprise-ready, repeatable, version-controlled.

**Extensibility**: Generators are discovered via Python entry points, allowing custom deployment targets (OpenShift, AWS SageMaker, air-gapped registries) to be added as separate packages.

## Installation

```bash
pip install aissemble-inference-deploy
```

Or with uv:

```bash
uv add aissemble-inference-deploy
```

## Quick Start

Navigate to your project directory (containing a `models/` directory with your model configurations), then:

```bash
# Generate local deployment scripts
inference deploy init --target local

# Start MLServer locally
cd deploy/local && ./run-mlserver.sh
```

Or for containerized deployment:

```bash
# Generate Docker deployment configs
inference deploy init --target docker

# Build and run with Docker Compose
cd deploy/docker && docker-compose up --build
```

Or for Kubernetes:

```bash
# Generate Kubernetes manifests (uses Docker image from above)
inference deploy init --target docker --target kubernetes

# Build Docker image, then deploy to K8s
docker build -t my-app:latest -f deploy/docker/Dockerfile .
kubectl apply -k deploy/kubernetes/base
```

Or for KServe (serverless ML with scale-to-zero):

```bash
# Generate KServe manifests (uses Docker image from above)
inference deploy init --target kserve

# Build and push Docker image, then deploy to KServe
docker build -t my-registry/my-app:v1.0.0 -f deploy/docker/Dockerfile .
docker push my-registry/my-app:v1.0.0
kubectl apply -f deploy/kserve/serving-runtime.yaml
kubectl apply -f deploy/kserve/inference-service.yaml
```

## CLI Reference

### `inference deploy init`

Initialize deployment configurations for your models.

```bash
inference deploy init [OPTIONS]
```

**Options:**
- `--target, -t` - Deployment target(s) to generate (default: local). Can be specified multiple times.
- `--model-dir, -m` - Path to models directory (default: ./models)
- `--output-dir, -o` - Output directory for generated configs (default: ./deploy)
- `--project-dir, -p` - Project root directory (default: current directory)

**Examples:**

```bash
# Generate local deployment only
inference deploy init --target local

# Generate Docker deployment
inference deploy init --target docker

# Generate Kubernetes manifests
inference deploy init --target kubernetes

# Generate KServe manifests (serverless ML)
inference deploy init --target kserve

# Generate multiple targets
inference deploy init --target local --target docker --target kubernetes --target kserve

# Generate for all available targets
inference deploy init --target all
```

### `inference deploy list-targets`

List available deployment targets. Generators are discovered via entry points.

```bash
inference deploy list-targets
```

## Built-in Generators

| Target | Description | Status |
|--------|-------------|--------|
| `local` | Local MLServer scripts for development | Available |
| `docker` | Containerized deployment with Docker Compose | Available |
| `kubernetes` | Standard K8s Deployment + Service with Kustomize | Available |
| `kserve` | KServe InferenceService with scale-to-zero | Available |

## Generated Output Structure

After running `inference deploy init`, your project will have:

```
your-project/
  models/
    your-model/
      model-settings.json
  deploy/
    .inference-deploy.yaml          # Tracks generation metadata
    local/
      run-mlserver.sh         # Start MLServer locally
      README.md               # Local deployment instructions
    docker/
      Dockerfile              # Multi-stage build for MLServer
      docker-compose.yml      # Local container testing
      .dockerignore           # Build context exclusions
      README.md               # Docker deployment instructions
    kubernetes/
      base/
        deployment.yaml       # K8s Deployment with health checks
        service.yaml          # ClusterIP Service
        kustomization.yaml    # Kustomize base config
      overlays/
        dev/
          kustomization.yaml  # Dev overlay (1 replica, lower resources)
        prod/
          kustomization.yaml  # Prod overlay (2 replicas, higher resources)
      README.md               # Kubernetes deployment instructions
    kserve/
      serving-runtime.yaml    # KServe ServingRuntime (shared runtime config)
      inference-service.yaml  # KServe InferenceService with scale-to-zero
      README.md               # KServe deployment instructions
```

**Note:** The Kubernetes and KServe generators use the Docker image built by the Docker generator. This keeps things DRY - the Dockerfile is defined once and reused across Docker Compose, Kubernetes, and KServe deployments.

## Configuration Tracking

The `.inference-deploy.yaml` file tracks:
- Generator version used
- When configs were generated
- Which targets were generated
- Checksums of generated files (for future update/merge functionality)

## Creating Custom Generators

Custom generators can be added via the `inference.generators` entry point. This is useful for:
- Air-gapped environments with internal registries
- Platform-specific deployments (OpenShift, AWS SageMaker, etc.)
- Organization-specific deployment patterns

### Step 1: Create Your Generator

```python
# my_org_deploy/openshift.py
from aissemble_inference_deploy import Generator, ModelInfo
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
[project.entry-points."inference.generators"]
openshift = "my_org_deploy.openshift:OpenShiftGenerator"
```

### Step 3: Install and Use

```bash
pip install my-org-deploy
inference deploy list-targets  # Shows 'openshift' alongside built-in targets
inference deploy init --target openshift
```

## License

Apache 2.0
