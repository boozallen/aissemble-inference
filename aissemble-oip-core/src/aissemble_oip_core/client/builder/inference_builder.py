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
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #L%
###
from abc import ABC, abstractmethod
from typing import Dict, Generator, Any
from collections.abc import Iterator

from aissemble_oip_core.client.oip_adapter import OipAdapter
from aissemble_oip_core.client.predictor import Predictor
from aissemble_oip_core.client.translator import Translator


class InferenceBuilder(ABC, Iterator[Any]):
    """Abstract base class for building task-specific inference clients.

    Rather than exposing a generic ``predict`` method, this class encourages the definition
    of task-oriented inference builders (e.g., object detection, text summarization, translation).
    Each concrete subclass can provide a natural, fluent API tailored to its task while
    sharing common configuration state and behavior.

    This design promotes:
    - Compile-time safety through task-specific method signatures
    - Reusable shared state (model name, adapter, parameters, etc.)
    - Consistent access to streaming and iteration capabilities
    - Alignment with concepts like HuggingFace "tasks"

    Concrete subclasses should implement ``build_predictor`` to return a fully configured
    :class:`Predictor` instance ready for inference.
    """

    def __init__(self) -> None:
        self._model_name: str | None = None
        self._oip_adapter: OipAdapter | None = None
        self._translator: Translator | None = None
        self._parameters: Dict[str, Any] = {}
        self._streaming: bool = False

    # -------------------------------------------------------------------------
    # Protected properties (intended for use by subclasses and fluent setters)
    # -------------------------------------------------------------------------

    @property
    def model_name(self) -> str | None:
        """The name or identifier of the model to be used for inference."""
        return self._model_name

    @property
    def oip_adapter(self) -> OipAdapter | None:
        """The OIP adapter responsible for communication with the inference service."""
        return self._oip_adapter

    @property
    def translator(self) -> Translator | None:
        """The translator that handles data format conversion between client and service."""
        return self._translator

    @property
    def parameters(self) -> Dict[str, Any]:
        """Task-specific or model-specific inference parameters."""
        return self._parameters

    @property
    def streaming(self) -> bool:
        """Whether the inference should be performed in streaming mode."""
        return self._streaming

    # -------------------------------------------------------------------------
    # Fluent configuration methods (to be implemented/chained by subclasses)
    # -------------------------------------------------------------------------

    def with_model(self, model_name: str) -> "InferenceBuilder":
        """Set the model name/identifier.

        Args:
            model_name: The identifier of the model to use.

        Returns:
            Self, for method chaining.
        """
        self._model_name = model_name
        return self

    def with_adapter(self, adapter: OipAdapter) -> "InferenceBuilder":
        """Set the OIP adapter instance.

        Args:
            adapter: The adapter handling protocol communication.

        Returns:
            Self, for method chaining.
        """
        self._oip_adapter = adapter
        return self

    def with_translator(self, translator: Translator) -> "InferenceBuilder":
        """Set the data translator instance.

        Args:
            translator: The translator for request/response serialization.

        Returns:
            Self, for method chaining.
        """
        self._translator = translator
        return self

    def with_parameters(self, **parameters: Any) -> "InferenceBuilder":
        """Add or update inference parameters.

        Args:
            **parameters: Arbitrary keyword arguments representing inference parameters.

        Returns:
            Self, for method chaining.
        """
        self._parameters.update(parameters)
        return self

    # -------------------------------------------------------------------------
    # Public API required by all task-specific builders
    # -------------------------------------------------------------------------

    @abstractmethod
    def build_predictor(self) -> Predictor:
        """Construct and return a fully configured :class:`Predictor` instance.

        Concrete subclasses must implement this method to assemble the predictor
        using the configured model name, adapter, translator, parameters, etc.

        Returns:
            A ready-to-use predictor for the specific task.
        """
        raise NotImplementedError

    def stream(self) -> "InferenceBuilder":
        """Enable streaming mode for subsequent inference calls.

        Returns:
            Self, for method chaining.
        """
        self._streaming = True
        return self

    # -------------------------------------------------------------------------
    # Iterator protocol support (for streaming responses)
    # -------------------------------------------------------------------------

    def __iter__(self) -> Generator[Any, None, None]:
        """Return a generator that yields streaming results.

        When streaming is enabled, calling ``iter(builder)`` or using the builder
        in a for-loop should yield incremental results from the inference service.

        The default implementation raises ``NotImplementedError``; concrete
        task-specific builders that support streaming should override this method.

        Yields:
            Task-specific streaming chunks (e.g., tokens, bounding boxes, etc.).
        """
        raise NotImplementedError(
            "Streaming iteration is not implemented for this task"
        )
