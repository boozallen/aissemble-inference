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
"""Translator for text summarization tasks."""

from aissemble_inference_core.client.oip_adapter import (
    OipRequest,
    OipResponse,
    TensorData,
)
from aissemble_inference_core.client.results.summarization_result import (
    SummarizationResult,
)
from aissemble_inference_core.client.translator import Translator


class DefaultSummarizationTranslator(Translator[str, SummarizationResult]):
    """Default translator for text summarization inference.

    This translator converts input text to OIP format and parses OIP responses
    into SummarizationResult objects. It is the only component aware of the
    OIP JSON schema and tensor details for summarization.

    The translator is configurable to work with different model implementations
    that may use different tensor names or parameter conventions.
    """

    def __init__(
        self,
        input_name: str = "text",
        output_name: str = "summary",
    ):
        """Initialize the summarization translator.

        Args:
            input_name: Name of the input tensor (default: "text")
            output_name: Name of the output tensor (default: "summary")
        """
        self.input_name = input_name
        self.output_name = output_name
        self._original_text: str = ""

    def preprocess(self, text: str) -> OipRequest:
        """Convert input text to OIP request format.

        Args:
            text: The text to summarize

        Returns:
            OipRequest with text as BYTES tensor

        Raises:
            ValueError: If text is empty or invalid
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")

        self._original_text = text

        # Encode text as UTF-8 bytes
        text_bytes = text.encode("utf-8")
        text_str = text_bytes.decode("utf-8")

        tensor = TensorData(
            name=self.input_name,
            shape=[1],
            datatype="BYTES",
            data=[text_str],
        )

        return OipRequest(inputs=[tensor])

    def postprocess(self, response: OipResponse) -> SummarizationResult:
        """Convert OIP response to SummarizationResult.

        Args:
            response: OIP response containing summary tensor

        Returns:
            SummarizationResult with extracted summary and metadata

        Raises:
            ValueError: If response format is invalid
        """
        outputs = {out.name: out for out in response.outputs}

        if self.output_name not in outputs:
            raise ValueError(
                f"Expected output tensor '{self.output_name}' not found in response. "
                f"Available: {list(outputs.keys())}"
            )

        summary_tensor = outputs[self.output_name]
        summary_data = self._extract_text(summary_tensor)

        if not summary_data:
            raise ValueError("Summary output is empty")

        return SummarizationResult(
            summary=summary_data,
            original_length=len(self._original_text),
            summary_length=len(summary_data),
            model_name=response.model_name,
        )

    def _extract_text(self, tensor: TensorData) -> str:
        """Extract text string from tensor data.

        Args:
            tensor: TensorData containing text

        Returns:
            Extracted text string
        """
        if not tensor.data:
            return ""

        # Handle nested list structure [[text]] or flat [text]
        data = tensor.data
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], list) and len(data[0]) > 0:
                text = data[0][0]
            else:
                text = data[0]

            if isinstance(text, str):
                return text
            elif isinstance(text, bytes):
                return text.decode("utf-8")

        return str(data)
