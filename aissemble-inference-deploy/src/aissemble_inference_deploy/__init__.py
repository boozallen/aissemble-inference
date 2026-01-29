###
# #%L
# aiSSEMBLE::Open Inference Protocol::Modules::deploy
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
"""
aiSSEMBLE OIP Deploy - Deployment tooling for OIP-compatible models.

This module provides CLI tooling to generate deployment configurations
for any OIP-compatible model across multiple deployment targets:
- Local (MLServer)
- Docker
- Kubernetes (vanilla)
- KServe (serverless)

Custom generators can be added via the 'inference.generators' entry point group.
"""

__version__ = "1.5.0.dev"

from .generators.base import Generator, ModelInfo
from .registry import GeneratorRegistry

__all__ = ["Generator", "GeneratorRegistry", "ModelInfo", "__version__"]
