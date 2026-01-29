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
from typing import Dict, Any


class RawInferenceBuilder:
    """A minimal, non-fluent interface for directly supplying raw tensors and parameters to an inference request.

    This class is intentionally designed to be "ugly" and low-level compared to higher-level task-specific builders.
    Its purpose is to support rare cases where pre-defined abstractions do not suffice (e.g., custom model signatures
    or experimental tasks). Use of this class should be considered a signal that a new, higher-level abstraction
    specific to the task or model should be contributed upstream or maintained in the project.

    The interface is deliberately non-fluent: each configuration method returns ``None`` rather than ``self``,
    discouraging method chaining and accidental use in place of more ergonomic APIs.
    """

    def __init__(self) -> None:
        """Initialize an empty raw inference request builder."""
        self._inputs: Dict[str, Any] = {}
        self._parameters: Dict[str, Any] = {}

    def inputs(self, tensors: Dict[str, Any]) -> None:
        """Set the raw input tensors for the inference request.

        Args:
            tensors: A mapping of input names to tensor objects (or compatible representations such as NumPy arrays,
                PyTorch tensors, TensorFlow tensors, etc.). The exact type requirements depend on the backend
                implementation.

        Returns:
            None. This method intentionally does not support fluent chaining.
        """
        if not isinstance(tensors, dict):
            raise TypeError(
                "tensors must be a dictionary mapping input names to tensor objects"
            )
        self._inputs = tensors.copy()

    def parameters(self, parameters: Dict[str, Any]) -> None:
        """Set optional inference parameters (e.g., temperature, top_k, etc.).

        Args:
            parameters: A mapping of parameter names to their values. Meaning and supported keys are model-specific.

        Returns:
            None. This method intentionally does not support fluent chaining.
        """
        if not isinstance(parameters, dict):
            raise TypeError("parameters must be a dictionary")
        self._parameters = parameters.copy()

    def run(self) -> Dict[str, Any]:
        """Execute the inference request using the configured raw inputs and parameters.

        This method delegates to the underlying client/runner implementation (assumed to be available
        in the broader library context).

        Returns:
            The raw model outputs, typically a dictionary mapping output names to tensor-like objects.

        Raises:
            RuntimeError: If the request cannot be executed (e.g., missing client context, network error, etc.).
            NotImplementedError: Placeholder until the actual execution logic is wired in by the library.
        """
        # Placeholder implementation – actual execution will be provided by integration with the client
        raise NotImplementedError(
            "RawInferenceBuilder.run() is not yet implemented. "
            "This method should be overridden or wired to the inference client in the final library."
        )

    # Optional helper for inspection/debugging
    def _get_request_payload(self) -> Dict[str, Any]:
        """Internal helper to retrieve the current payload (used by tests or client integration)."""
        return {
            "inputs": self._inputs,
            "parameters": self._parameters,
        }
