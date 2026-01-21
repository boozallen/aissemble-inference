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
"""aiSSEMBLE OIP Common Test Utilities.

Reusable MLServer test fixtures and utilities for aiSSEMBLE OIP modules and examples.
"""

from .behave_helpers import (
    setup_mlserver_dynamic,
    setup_mlserver_simple,
    start_mlserver_with_model,
    teardown_mlserver,
)
from .config_builder import create_model_settings, create_settings
from .mlserver_fixture import MLServerFixture

__all__ = [
    "MLServerFixture",
    "create_settings",
    "create_model_settings",
    "setup_mlserver_simple",
    "setup_mlserver_dynamic",
    "start_mlserver_with_model",
    "teardown_mlserver",
]
