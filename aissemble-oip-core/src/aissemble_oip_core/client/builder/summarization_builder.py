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
"""Builder for text summarization inference."""

from typing import Any, Generator

from aissemble_oip_core.client.builder.inference_builder import InferenceBuilder
from aissemble_oip_core.client.predictor import Predictor
from aissemble_oip_core.client.results.summarization_result import SummarizationResult
from aissemble_oip_core.client.translators.summarization_translator import (
    DefaultSummarizationTranslator,
)


class SummarizationPredictor(Predictor[str, SummarizationResult]):
    """Concrete predictor implementation for text summarization."""

    def __init__(
        self,
        adapter: Any,
        translator: DefaultSummarizationTranslator,
    ):
        """Initialize the summarization predictor.

        Args:
            adapter: OIP adapter for communication
            translator: Translator for preprocessing/postprocessing
        """
        self.adapter = adapter
        self.translator = translator

    def predict(self, text: str) -> SummarizationResult:  # noqa: A003
        """Perform summarization on the input text.

        Args:
            text: Text to summarize

        Returns:
            SummarizationResult with generated summary
        """
        request = self.translator.preprocess(text)
        response = self.adapter.infer(request)
        return self.translator.postprocess(response)


class SummarizationBuilder(InferenceBuilder):
    """Task-specific builder for text summarization inference.

    Provides a fluent, natural API for text summarization:
        builder.text("long text...").max_length(100).run()

    Example:
        client = InferenceClient(adapter, endpoint)
        result = (client.summarize("bart-large")
                       .text("Very long article text here...")
                       .max_length(150)
                       .min_length(50)
                       .run())
        print(result.summary)
        print(f"Compressed {result.compression_ratio:.1f}x")
    """

    def __init__(self):
        """Initialize the summarization builder."""
        super().__init__()
        self._text_input: str | None = None
        self._max_length: int | None = None
        self._min_length: int | None = None

    def text(self, text: str) -> "SummarizationBuilder":
        """Set the input text to summarize.

        Args:
            text: The text to summarize

        Returns:
            Self for method chaining

        Raises:
            ValueError: If text is empty or not a string
        """
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        self._text_input = text
        return self

    def max_length(self, length: int) -> "SummarizationBuilder":
        """Set maximum summary length.

        Args:
            length: Maximum length in tokens or characters (model-dependent)

        Returns:
            Self for method chaining

        Raises:
            ValueError: If length is not positive
        """
        if length <= 0:
            raise ValueError("Max length must be positive")
        self._max_length = length
        return self

    def min_length(self, length: int) -> "SummarizationBuilder":
        """Set minimum summary length.

        Args:
            length: Minimum length in tokens or characters (model-dependent)

        Returns:
            Self for method chaining

        Raises:
            ValueError: If length is not positive
        """
        if length <= 0:
            raise ValueError("Min length must be positive")
        self._min_length = length
        return self

    def run(self) -> SummarizationResult:
        """Execute the text summarization inference.

        Returns:
            SummarizationResult with generated summary

        Raises:
            ValueError: If required inputs are missing or invalid
        """
        if self._text_input is None:
            raise ValueError("Text input is required. Call .text() first.")

        if self._min_length and self._max_length:
            if self._min_length > self._max_length:
                raise ValueError(
                    f"Min length ({self._min_length}) cannot exceed "
                    f"max length ({self._max_length})"
                )

        # Add length parameters to request if specified
        if self._max_length is not None:
            self._parameters["max_length"] = self._max_length
        if self._min_length is not None:
            self._parameters["min_length"] = self._min_length

        predictor = self.build_predictor()
        return predictor.predict(self._text_input)

    def build_predictor(self) -> Predictor[str, SummarizationResult]:
        """Build the predictor for summarization.

        Returns:
            SummarizationPredictor instance

        Raises:
            ValueError: If adapter is not set
        """
        if self.oip_adapter is None:
            raise ValueError("OipAdapter is required. Call .with_adapter() first.")

        translator = (
            self.translator
            if isinstance(self.translator, DefaultSummarizationTranslator)
            else DefaultSummarizationTranslator()
        )

        return SummarizationPredictor(
            adapter=self.oip_adapter,
            translator=translator,
        )

    def __iter__(self) -> Generator[SummarizationResult, None, None]:
        """Streaming iteration for summarization.

        Not currently implemented for summarization tasks.

        Raises:
            NotImplementedError: Streaming is not yet supported
        """
        raise NotImplementedError(
            "Streaming is not yet supported for summarization tasks"
        )

    def __next__(self) -> SummarizationResult:
        """Return the next streaming result.

        Not currently implemented for summarization tasks.

        Raises:
            NotImplementedError: Streaming is not yet supported
        """
        raise NotImplementedError(
            "Streaming is not yet supported for summarization tasks"
        )
