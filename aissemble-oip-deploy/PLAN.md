# Plan: Write Once, Deploy Many - Deployment Tooling

## Overview

Create a new module **`aissemble-oip-deploy`** that provides CLI tooling to generate deployment configurations for any OIP-compatible model. Users run a command, get version-controlled configs in their project, and can re-run to update while preserving customizations.

**Key Value**: Not just "possible to deploy" but "easy to deploy" - enterprise-ready, repeatable, version-controlled.

**Extensibility**: Generators are discovered via Python entry points (`oip.generators`), allowing custom deployment targets (OpenShift, AWS SageMaker, air-gapped registries) to be added as separate packages without modifying the core deploy module.

**Project Structure**: `aissemble-oip-deploy` is a **peer to aissemble-oip-core** (not under aissemble-oip-modules) because it's a framework that others extend, similar to how core provides the client framework.

---

## Incremental Phases (for team review)

| Phase | Scope | Deliverable | Status |
|-------|-------|-------------|--------|
| **Phase A** | Module skeleton + Local generator | `oip deploy init --target local` works | **COMPLETE** |
| **Phase B** | Docker generator | `oip deploy init --target docker` works | **COMPLETE** |
| **Phase C** | Kubernetes vanilla generator | `oip deploy init --target kubernetes` works | Not started |
| **Phase D** | KServe generator | `oip deploy init --target kserve` works | Not started |
| **Phase E** | Update/merge workflow | `oip deploy update` with conflict detection | Not started |
| **Phase F** | Example project + docs | Complete example + documentation | Not started |

Each phase is independently reviewable and delivers working functionality.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     User's Model Project                        │
│  ┌─────────────┐    ┌─────────────────────────────────────────┐ │
│  │ models/     │    │ deploy/  (generated, version-controlled)│ │
│  │ sumy-textrank/   │   docker/                               │ │
│  │   model-settings.json   kubernetes/                        │ │
│  └─────────────┘    │   local/                                │ │
│                     └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
         ▲
         │ oip deploy init / oip deploy update
         │
┌────────┴────────────────────────────────────────────────────────┐
│              aissemble-oip-deploy (framework)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │ CLI commands │  │ Registry     │  │ Built-in Generators   │  │
│  │ oip deploy   │  │ discovers    │  │ local, docker, k8s    │  │
│  │              │  │ generators   │  │ (via entry points)    │  │
│  └──────────────┘  └──────────────┘  └───────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         ▲
         │ oip.generators entry point
         │
┌────────┴────────────────────────────────────────────────────────┐
│              Custom Generator Packages (optional)               │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │ my-org-openshift │  │ my-org-sagemaker │                     │
│  │ (entry point)    │  │ (entry point)    │                     │
│  └──────────────────┘  └──────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

## Deployment Targets

| Target | Purpose | Local Testing |
|--------|---------|---------------|
| Local MLServer | Development | `mlserver start models/` |
| Docker | Containerized deployment | `docker-compose up` |
| Kubernetes (vanilla) | Standard K8s Deployment + Service | Rancher Desktop |
| KServe | Serverless on K8s (scale-to-zero) | Rancher Desktop + KServe |

## CLI Interface

```bash
# Initialize deployment configs in user's project
oip deploy init --target docker --target kubernetes --target kserve

# Update existing configs (merge conflicts if customizations exist)
oip deploy update

# Generate for specific model
oip deploy init --model-dir ./models/sumy-textrank --target docker

# List available targets
oip deploy list-targets

# Validate generated configs
oip deploy validate
```

## Module Structure (Current State After Phase A)

```
aissemble-oip-deploy/           # Peer to aissemble-oip-core (NOT under modules)
  README.md                     # User documentation + extensibility guide
  PLAN.md                       # This file
  pyproject.toml                # With CLI + generator entry points
  pom.xml                       # Maven build config

  src/aissemble_oip_deploy/
    __init__.py                 # Exports Generator, GeneratorRegistry, ModelInfo
    cli.py                      # Click-based CLI commands
    config.py                   # .oip-deploy.yaml handling
    registry.py                 # Entry point discovery (oip.generators)

    generators/
      __init__.py
      base.py                   # Abstract Generator class
      local.py                  # Local MLServer generator (registered via entry point)
      docker.py                 # Docker generator (registered via entry point)
      # kubernetes.py           # Phase C
      # kserve.py               # Phase D

      templates/
        local/
          run-mlserver.sh.j2
        docker/
          Dockerfile.j2
          docker-compose.yml.j2
          .dockerignore.j2
        # kubernetes/           # Phase C
        # kserve/               # Phase D

      # merge.py                # Phase E - Config merge/conflict detection

    tests/
      features/                 # Phase F - BDD tests
```

## Generated Output Structure (in user's project)

```
user-project/
  models/
    sumy-textrank/
      model-settings.json

  deploy/                        # Generated by 'oip deploy init'
    .oip-deploy.yaml            # Tracks generation metadata & versions

    local/
      run-mlserver.sh           # Start MLServer locally
      README.md                 # Local deployment instructions

    docker/                     # Phase B
      Dockerfile                # Multi-stage build
      docker-compose.yml        # Local container testing
      .dockerignore
      README.md                 # Docker deployment instructions

    kubernetes/                 # Phase C
      base/
        deployment.yaml         # K8s Deployment
        service.yaml            # K8s Service
        kustomization.yaml      # Kustomize base
      overlays/
        dev/
          kustomization.yaml    # Dev environment overlay
        prod/
          kustomization.yaml    # Prod environment overlay
      README.md                 # K8s deployment instructions

    kserve/                     # Phase D
      inference-service.yaml    # KServe InferenceService
      README.md                 # KServe deployment instructions
```

---

## Detailed Phase Breakdowns

### Phase A: Module Skeleton + Local Generator - COMPLETE

**Delivered:**
1. `aissemble-oip-deploy/` module as **peer to aissemble-oip-core** (not under modules)
2. CLI with `oip deploy init --target local` and `oip deploy list-targets`
3. `registry.py` - **Entry point discovery** for generators (`oip.generators` group)
4. `generators/base.py` - abstract Generator class with model discovery
5. `generators/local.py` - LocalGenerator implementation (registered via entry point)
6. `templates/local/run-mlserver.sh.j2` template
7. `config.py` - `.oip-deploy.yaml` tracking with checksums
8. Public exports: `Generator`, `GeneratorRegistry`, `ModelInfo` for custom generators

**Entry Point Registration:**
```toml
# pyproject.toml
[project.entry-points."oip.generators"]
local = "aissemble_oip_deploy.generators:LocalGenerator"
```

**Verified:**
- CLI works: `oip deploy init --target local`
- Entry point discovery works: `oip deploy list-targets` shows generators with descriptions
- Tested against `aissemble-summarization-example` - found sumy-textrank and sumy-lsa models
- Maven build passes

---

### Phase B: Docker Generator

**Goal**: Add Docker deployment capability.

**Deliverables**:
1. `generators/docker.py` implementation
2. Docker templates: `Dockerfile.j2`, `docker-compose.yml.j2`, `.dockerignore.j2`
3. Model detection: read `model-settings.json` to determine runtime dependencies

**Files to Create**:
```
src/aissemble_oip_deploy/
  generators/docker.py
  templates/docker/
    Dockerfile.j2
    docker-compose.yml.j2
    .dockerignore.j2
```

**Template Considerations**:
- Multi-stage build for smaller images
- Parameterized base image (Python version)
- Copy models directory
- Install runtime dependencies based on model-settings.json
- Expose correct port

**Verification**:
```bash
oip deploy init --target docker
cd deploy/docker
docker-compose up --build
# Test endpoint works
```

---

### Phase C: Kubernetes Vanilla Generator

**Goal**: Add standard Kubernetes Deployment + Service generation.

**Deliverables**:
1. `generators/kubernetes.py` implementation
2. K8s templates with Kustomize structure
3. Dev/prod overlay generation

**Files to Create**:
```
src/aissemble_oip_deploy/
  generators/kubernetes.py
  templates/kubernetes/
    deployment.yaml.j2
    service.yaml.j2
    kustomization.yaml.j2
    overlays/
      dev/kustomization.yaml.j2
      prod/kustomization.yaml.j2
```

**Template Considerations**:
- Parameterized resource limits (CPU, memory)
- Configurable replicas
- Health checks (readiness/liveness probes)
- ConfigMap for model settings
- Service type (ClusterIP, LoadBalancer, NodePort)

**Verification**:
```bash
oip deploy init --target kubernetes
# On Rancher Desktop:
kubectl apply -k deploy/kubernetes/base
kubectl get pods
# Test endpoint
```

---

### Phase D: KServe Generator

**Goal**: Add KServe InferenceService generation for serverless ML.

**Deliverables**:
1. `generators/kserve.py` implementation
2. KServe InferenceService template
3. Scale-to-zero configuration

**Files to Create**:
```
src/aissemble_oip_deploy/
  generators/kserve.py
  templates/kserve/
    inference-service.yaml.j2
```

**Template Considerations**:
- Custom predictor with MLServer image
- Scale-to-zero annotations
- Min/max replicas
- Resource requests/limits
- Storage URI for models (optional)

**Verification**:
```bash
oip deploy init --target kserve
# On Rancher Desktop with KServe installed:
kubectl apply -f deploy/kserve/inference-service.yaml
kubectl get inferenceservice
# Verify scale-to-zero works
```

---

### Phase E: Update/Merge Workflow

**Goal**: Enable safe regeneration with conflict detection.

**Deliverables**:
1. `merge.py` with checksum-based conflict detection
2. Enhanced `config.py` with file checksums in `.oip-deploy.yaml`
3. `oip deploy update` command with interactive prompts
4. `oip deploy validate` for config validation

**Files to Create/Modify**:
```
src/aissemble_oip_deploy/
  merge.py (new)
  config.py (enhanced - already has checksum support)
  cli.py (add update, validate commands)
```

**Merge Logic**:
1. Load `.oip-deploy.yaml` to get original checksums
2. For each tracked file:
   - Compute current checksum
   - If matches original: safe to overwrite
   - If different: user modified, prompt for action
3. Actions: overwrite, skip, show diff, merge (if possible)

**Verification**:
```bash
# Generate, modify, then update
oip deploy init --target docker
echo "# Custom comment" >> deploy/docker/Dockerfile
oip deploy update
# Should prompt: "Dockerfile modified. Merge? [y/n/diff]"
```

---

### Phase F: Example Project + Documentation

**Goal**: Complete example and comprehensive documentation.

**Deliverables**:
1. `aissemble-multi-deploy-example/` project
2. Module README with CLI reference
3. Example README with walkthrough
4. BDD tests for generators

**Files to Create**:
```
aissemble-oip-examples/aissemble-multi-deploy-example/
  pom.xml
  pyproject.toml
  README.md
  Makefile
  models/
    settings.json
    sumy-textrank/model-settings.json
  scripts/test-endpoint.py
  deploy/  # Generated by oip deploy init --target all

aissemble-oip-modules/aissemble-oip-deploy/
  tests/features/deploy_generation.feature
  tests/features/config_merge.feature
```

**Verification**:
```bash
# Full workflow in example
cd aissemble-oip-examples/aissemble-multi-deploy-example
make local-test      # Local works
make docker-test     # Docker works
make k8s-test        # K8s works
make kserve-test     # KServe works
```

---

## Key Design Decisions

1. **Click for CLI**: Standard Python CLI framework, familiar to most developers
2. **Jinja2 for templates**: Powerful, widely used, easy to customize
3. **Checksum tracking**: Detect user modifications via SHA256 of generated content
4. **Kustomize for K8s**: Industry-standard approach for environment overlays
5. **Single entry point**: `oip` command namespace for all OIP tooling

## Prerequisites Documentation

README should document:
- **Local**: Python 3.11, uv/pip
- **Docker**: Docker Desktop or Rancher Desktop
- **Kubernetes**: kubectl + Rancher Desktop (or other local K8s)
- **KServe**: Rancher Desktop + KServe addon

## Success Criteria

1. **CLI Usability**: `oip deploy init` generates working configs in under 5 seconds
2. **Write Once**: `SumyRuntime` code unchanged across all deployments
3. **Version Control**: Generated configs are clean, well-documented, and git-friendly
4. **Update Safety**: `oip deploy update` detects and prompts for conflicts
5. **Same Interface**: Same OIP request/response works against all endpoints
6. **Documentation**: Each generated README explains deployment steps clearly
7. **Rancher Desktop**: K8s instructions assume Rancher Desktop as default
