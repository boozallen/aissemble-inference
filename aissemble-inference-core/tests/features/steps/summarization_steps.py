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
"""Step definitions for text summarization functionality."""

from unittest.mock import Mock

from behave import given, then, when

from aissemble_inference_core.client.inference_client import InferenceClient
from aissemble_inference_core.client.oip_adapter import (
    OipAdapter,
    OipResponse,
    TensorData,
)


@given("an text on which we would like to perform summarization")
def step_given_text_for_summarization(context):
    """Create sample text for summarization."""
    context.sample_text = (
        "Machine learning is a subset of artificial intelligence. " * 10
    )


@when("the text is processed for summarization")
def step_when_process_text_for_summarization(context):
    """Process text using a mocked OIP endpoint."""
    mock_adapter = Mock(spec=OipAdapter)

    mock_response = OipResponse(
        model_name="summarization-model",
        outputs=[
            TensorData(
                name="summary",
                shape=[1],
                datatype="BYTES",
                data=[
                    [
                        "Machine learning is a key AI technique used in modern applications."
                    ]
                ],
            )
        ],
    )

    mock_adapter.infer.return_value = mock_response

    client = InferenceClient(adapter=mock_adapter, endpoint="http://test:8080")
    context.result = client.summarize().text(context.sample_text).run()


@then("a summary is returned with a summary length")
def step_then_verify_summarization_result(context):
    """Verify the summarization result contains expected data."""
    assert context.result is not None
    assert context.result.summary is not None
    assert len(context.result.summary) > 0
    assert context.result.summary_length > 0
    assert context.result.original_length > 0
