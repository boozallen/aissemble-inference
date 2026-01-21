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
"""Step definitions for object detection functionality."""

from io import BytesIO
from unittest.mock import Mock

from behave import given, then, when
from PIL import Image

from aissemble_oip_core.client.inference_client import InferenceClient
from aissemble_oip_core.client.oip_adapter import OipAdapter, OipResponse, TensorData


@given("an image on which we would like to perform object detection")
def step_given_image_for_detection(context):
    """Create a test image for object detection."""
    image = Image.new("RGB", (640, 480), color="blue")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    context.test_image = buffer.getvalue()


@when("the image is processed for object detection")
def step_when_process_image_for_detection(context):
    """Process the image using a mocked OIP endpoint."""

    def mock_infer(request):
        """Mock infer that preserves request parameters in response."""
        return OipResponse(
            model_name="test-object-detection-model",
            outputs=[
                TensorData(
                    name="bboxes",
                    shape=[1, 4],
                    datatype="FP32",
                    data=[[[100.0, 150.0, 300.0, 400.0]]],
                ),
                TensorData(
                    name="labels",
                    shape=[1],
                    datatype="BYTES",
                    data=[["person"]],
                ),
                TensorData(
                    name="scores",
                    shape=[1],
                    datatype="FP32",
                    data=[[0.95]],
                ),
            ],
            parameters=request.parameters,  # Preserve request parameters
        )

    mock_adapter = Mock(spec=OipAdapter)
    mock_adapter.infer.side_effect = mock_infer

    client = InferenceClient(adapter=mock_adapter, endpoint="http://test:8080")
    context.result = client.detect_object().image(context.test_image).run()


@then(
    "a result is returned with detected objects and their associated labels, scores, and bounding box coordinates"
)
def step_then_verify_detection_result(context):
    """Verify the object detection result contains expected data."""
    assert context.result is not None
    assert len(context.result.detections) > 0

    detection = context.result.detections[0]

    assert detection.label is not None
    assert len(detection.label) > 0

    assert detection.confidence is not None
    assert 0.0 <= detection.confidence <= 1.0

    assert detection.bbox is not None
    assert detection.bbox.x1 >= 0
    assert detection.bbox.y1 >= 0
    assert detection.bbox.x2 > detection.bbox.x1
    assert detection.bbox.y2 > detection.bbox.y1
