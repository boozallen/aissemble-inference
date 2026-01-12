###
# #%L
# aiSSEMBLE::Open Inference Protocol::Core
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
"""Behave environment configuration for OIP Core tests.

This module provides setup and teardown hooks for behave test execution.
"""


def before_all(context):
    """Execute before all tests run.

    Args:
        context: Behave context object
    """
    context.test_data_dir = "tests/test_data"


def before_scenario(context, scenario):
    """Execute before each scenario.

    Args:
        context: Behave context object
        scenario: Current scenario being executed
    """
    pass


def after_scenario(context, scenario):
    """Execute after each scenario.

    Args:
        context: Behave context object
        scenario: Scenario that just completed
    """
    pass


def after_all(context):
    """Execute after all tests have run.

    Args:
        context: Behave context object
    """
    pass
