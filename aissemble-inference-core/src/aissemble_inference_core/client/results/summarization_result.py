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
"""Value objects for text summarization results."""

from dataclasses import dataclass


@dataclass
class SummarizationResult:
    """Result of a text summarization inference.

    This class encapsulates the output from a summarization model, including
    the generated summary text and optional metadata about the operation.

    Attributes:
        summary: The generated summary text
        original_length: Character count of the original input text
        summary_length: Character count of the generated summary
        model_name: Optional name of the model that generated the summary
        input_tokens: Optional count of input tokens (for token-based models)
        output_tokens: Optional count of output tokens (for token-based models)
    """

    summary: str
    original_length: int
    summary_length: int
    model_name: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None

    @property
    def compression_ratio(self) -> float:
        """Calculate the compression ratio (original length / summary length).

        Returns:
            Ratio of original to summary length. Higher values indicate more compression.
            Returns 0.0 if summary is empty.

        Example:
            >>> result = SummarizationResult(
            ...     summary="Short summary",
            ...     original_length=1000,
            ...     summary_length=100
            ... )
            >>> result.compression_ratio
            10.0
        """
        if self.summary_length == 0:
            return 0.0
        return self.original_length / self.summary_length

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return (
            f"SummarizationResult("
            f"summary={self.summary[:50]!r}..., "
            f"original_length={self.original_length}, "
            f"summary_length={self.summary_length}, "
            f"compression_ratio={self.compression_ratio:.2f}x"
            f")"
        )
