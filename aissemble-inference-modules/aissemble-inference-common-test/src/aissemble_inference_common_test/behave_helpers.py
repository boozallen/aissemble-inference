###
# #%L
# aiSSEMBLE::Open Inference Protocol::Common Test Utilities
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #L%
###
"""Behave integration helpers for MLServer testing.

Provides drop-in replacement functions for environment.py hooks,
maintaining backward compatibility with existing test code.
"""

from pathlib import Path
from typing import Any, Optional

from .mlserver_fixture import MLServerFixture


def setup_mlserver_simple(context: Any, models_dir: Path, port: int = 8080) -> None:
    """Setup MLServer fixture for static model directory (examples).

    Sets context attributes for backward compatibility:
    - context.mlserver_fixture
    - context.mlserver_url
    - context.mlserver_port

    Usage in before_all():
        setup_mlserver_simple(context, models_dir=Path("models"), port=8080)
        context.mlserver_fixture.start()

    Args:
        context: Behave context object
        models_dir: Path to existing models directory
        port: HTTP port (default: 8080)
    """
    context.mlserver_fixture = MLServerFixture.simple(port=port, models_dir=models_dir)
    context.mlserver_url = None  # Will be set after start()
    context.mlserver_port = None  # Will be set after start()
    context.mlserver_process = None  # Backward compatibility


def setup_mlserver_dynamic(context: Any) -> None:
    """Setup MLServer fixture for dynamic config generation (module tests).

    Sets context attributes for backward compatibility:
    - context.mlserver_fixture
    - context.mlserver_url
    - context.mlserver_port
    - context.mlserver_process
    - context.temp_dir

    Usage in before_all():
        setup_mlserver_dynamic(context)

    Args:
        context: Behave context object
    """
    context.mlserver_fixture = MLServerFixture.dynamic()
    context.mlserver_url = None  # Will be set after start_with_model()
    context.mlserver_port = None  # Will be set after start_with_model()
    context.mlserver_process = None  # Backward compatibility
    context.temp_dir = None  # Will be set after start_with_model()


def teardown_mlserver(context: Any) -> None:
    """Teardown MLServer fixture and cleanup resources.

    Usage in after_all():
        teardown_mlserver(context)

    Args:
        context: Behave context object
    """
    if hasattr(context, "mlserver_fixture"):
        fixture = context.mlserver_fixture
        if fixture.process:
            exit_code = fixture.process.poll()
            if exit_code is not None:
                stdout, stderr = fixture.process.communicate()
                print(f"\nMLServer exited with code {exit_code}")
                print(f"stdout: {stdout.decode()}")
                print(f"stderr: {stderr.decode()}")
            else:
                fixture.stop()

        fixture.cleanup()


def start_mlserver_with_model(
    context: Any,
    model_name: str,
    runtime: str,
    global_settings: Optional[dict] = None,
    **parameters,
) -> None:
    """Start MLServer with dynamically generated model configuration.

    Updates context attributes for backward compatibility:
    - context.mlserver_url
    - context.mlserver_port
    - context.mlserver_process
    - context.temp_dir

    Usage in test steps:
        start_mlserver_with_model(
            context,
            model_name="yolo",
            runtime="aissemble_inference_yolo.YOLORuntime",
            model="yolov8n.pt"
        )

    Args:
        context: Behave context object
        model_name: Model name (e.g., "yolo", "sumy")
        runtime: Runtime implementation class path
        global_settings: Optional global settings.json content
        **parameters: Model parameters for model-settings.json
    """
    if not hasattr(context, "mlserver_fixture"):
        raise RuntimeError("Call setup_mlserver_dynamic() in before_all() first")

    fixture = context.mlserver_fixture
    fixture.start_with_model(
        model_name=model_name,
        runtime=runtime,
        global_settings=global_settings,
        **parameters,
    )

    # Update context attributes for backward compatibility
    context.mlserver_url = fixture.url
    context.mlserver_port = fixture.port
    context.mlserver_process = fixture.process
    context.temp_dir = fixture.temp_dir
