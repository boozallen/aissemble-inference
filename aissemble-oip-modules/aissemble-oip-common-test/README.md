# aiSSEMBLE OIP Common Test Utilities

Reusable MLServer test utilities for aiSSEMBLE Open Inference Protocol modules and examples.

## Overview

This module provides consolidated MLServer lifecycle management utilities to eliminate code duplication across test suites. It offers two primary usage patterns:

1. **Simple mode**: For examples with static model directories
2. **Dynamic mode**: For module tests with temporary config generation

## Installation

```bash
# As a test dependency in pyproject.toml
[dependency-groups]
test = [
    "aissemble-oip-common-test",
]

[tool.uv.sources]
aissemble-oip-common-test = { path = "../aissemble-oip-common-test", editable = true }
```

## Usage

### Simple Mode (Examples)

For tests that use pre-configured model directories:

```python
# tests/features/environment.py
from pathlib import Path
from aissemble_oip_common_test.behave_helpers import (
    setup_mlserver_simple,
    teardown_mlserver,
)

def before_all(context):
    example_dir = Path(__file__).parent.parent.parent
    models_dir = example_dir / "models"

    setup_mlserver_simple(context, models_dir=models_dir, port=8080)
    context.mlserver_fixture.start()

def after_all(context):
    teardown_mlserver(context)
```

### Dynamic Mode (Module Tests)

For tests that generate model configurations dynamically:

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

# In your step definitions:
start_mlserver_with_model(
    context,
    model_name="yolo",
    runtime="aissemble_oip_yolo.YOLORuntime",
    model="yolov8n.pt"
)
```

## Features

- **Process Management**: Robust MLServer subprocess handling with zombie process detection
- **Health Checking**: Automatic polling of `/v2/health/ready` endpoint
- **Graceful Shutdown**: Terminate with timeout, then kill if needed (with safety timeouts)
- **Dynamic Port Allocation**: Automatic free port discovery
- **Config Generation**: JSON settings and model-settings creation
- **Context Manager Support**: Automatic cleanup with Python `with` statement
- **Error Logging**: Detailed warnings for cleanup and shutdown failures
- **Backward Compatible**: Drop-in replacement for existing test code

## API Reference

### MLServerFixture

Main fixture class for MLServer lifecycle management.

#### Basic Usage

```python
from aissemble_oip_common_test import MLServerFixture

# Simple mode
fixture = MLServerFixture.simple(port=8080, models_dir=Path("models"))
fixture.start()

# Dynamic mode
fixture = MLServerFixture.dynamic()
fixture.start_with_model(
    model_name="yolo",
    runtime="aissemble_oip_yolo.YOLORuntime",
    model="yolov8n.pt"
)

# Cleanup
fixture.stop()
fixture.cleanup()
```

#### Context Manager Usage (Recommended)

For automatic cleanup even when tests fail:

```python
from aissemble_oip_common_test import MLServerFixture
from pathlib import Path

# Simple mode with context manager
with MLServerFixture.simple(port=8080, models_dir=Path("models")) as fixture:
    fixture.start()
    # Run tests...
    # Automatic cleanup on exit

# Dynamic mode with context manager
with MLServerFixture.dynamic() as fixture:
    fixture.start_with_model(
        model_name="yolo",
        runtime="aissemble_oip_yolo.YOLORuntime",
        model="yolov8n.pt"
    )
    # Run tests...
    # Automatic stop() and cleanup() on exit, even if exception occurs
```

### Behave Helpers

- `setup_mlserver_simple(context, models_dir, port)` - Initialize simple fixture
- `setup_mlserver_dynamic(context)` - Initialize dynamic fixture
- `start_mlserver_with_model(context, model_name, runtime, **params)` - Start with config
- `teardown_mlserver(context)` - Cleanup and shutdown

## License

Apache 2.0
