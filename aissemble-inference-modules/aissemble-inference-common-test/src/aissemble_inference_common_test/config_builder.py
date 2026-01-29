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
"""MLServer configuration file builders.

Utilities for generating settings.json and model-settings.json files
for dynamic MLServer configuration during testing.
"""

import json
from pathlib import Path
from typing import Any, Dict


def create_settings(models_dir: Path, settings: Dict[str, Any]) -> None:
    """Create MLServer global settings.json file.

    Args:
        models_dir: Directory where settings.json will be written
        settings: Settings dictionary (parallel_workers, host, etc.)
    """
    settings_path = models_dir / "settings.json"
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)


def create_model_settings(model_dir: Path, model_settings: Dict[str, Any]) -> None:
    """Create model-settings.json file for a specific model.

    Args:
        model_dir: Model directory where model-settings.json will be written
        model_settings: Model configuration (name, implementation, parameters)
    """
    settings_path = model_dir / "model-settings.json"
    with open(settings_path, "w") as f:
        json.dump(model_settings, f, indent=2)
