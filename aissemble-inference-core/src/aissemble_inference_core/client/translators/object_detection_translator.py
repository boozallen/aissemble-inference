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
from typing import Any

from aissemble_inference_core.client.oip_adapter import (
    OipRequest,
    OipResponse,
    TensorData,
)
from aissemble_inference_core.client.results import (
    BoundingBox,
    Detection,
    ObjectDetectionResult,
)
from aissemble_inference_core.client.translator import Translator
from aissemble_inference_core.client.translators._image_utils import (
    encode_image_for_oip,
)
from aissemble_inference_core.client.translators._tensor_utils import (
    validate_required_tensors,
    validate_tensor_lengths_match,
)


class DefaultObjectDetectionTranslator(Translator[Any, ObjectDetectionResult]):
    """A reasonable default translator for object detection payloads.

    This translator handles:
    - Auto-encoding images to base64 bytes for OIP compatibility
    - Converting various image formats (PIL, numpy, file paths)
    - Parsing bounding box outputs in common formats
    - Creating ObjectDetectionResult with proper metadata

    The translator expects the model to output:
    - bboxes: [N, 4] tensor with coordinates (x1, y1, x2, y2)
    - labels: [N] tensor with class labels
    - scores: [N] tensor with confidence scores

    Thread Safety:
    This translator is thread-safe and stateless. Image dimensions are stored in
    request parameters and retrieved from response parameters.
    """

    def __init__(
        self,
        input_name: str = "image",
        bbox_output_name: str = "bboxes",
        label_output_name: str = "labels",
        score_output_name: str = "scores",
    ):
        """Initialize the translator with configurable tensor names.

        Args:
            input_name: Name of the input tensor (default: "image")
            bbox_output_name: Name of bounding box output tensor (default: "bboxes")
            label_output_name: Name of label output tensor (default: "labels")
            score_output_name: Name of score output tensor (default: "scores")
        """
        self.input_name = input_name
        self.bbox_output_name = bbox_output_name
        self.label_output_name = label_output_name
        self.score_output_name = score_output_name

    def preprocess(self, input_data: Any) -> OipRequest:  # noqa: A003
        """Preprocess image input into an OipRequest.

        Accepts various input formats:
        - PIL Image
        - numpy array
        - file path (string)
        - bytes

        Args:
            input_data: Image data in supported format

        Returns:
            OipRequest with encoded image tensor and dimensions in parameters
        """
        image_bytes, width, height = encode_image_for_oip(input_data)

        tensor = TensorData(
            name=self.input_name,
            shape=[1, len(image_bytes)],
            datatype="BYTES",
            data=[[image_bytes]],
        )

        # Store image dimensions in request parameters for stateless operation
        return OipRequest(
            inputs=[tensor],
            parameters={"_image_width": width, "_image_height": height},
        )

    def postprocess(self, response: OipResponse) -> ObjectDetectionResult:
        """Postprocess OipResponse into ObjectDetectionResult.

        Args:
            response: OIP response containing detection outputs and dimensions

        Returns:
            ObjectDetectionResult with parsed detections

        Raises:
            ValueError: If required tensors are missing or dimensions not available
        """
        outputs = {out.name: out for out in response.outputs}

        # Validate required tensors are present
        required = [
            self.bbox_output_name,
            self.label_output_name,
            self.score_output_name,
        ]
        validate_required_tensors(outputs, required, "Default object detection")

        # Get image dimensions from response parameters
        params = response.parameters or {}
        image_width = params.get("_image_width")
        image_height = params.get("_image_height")

        if image_width is None or image_height is None:
            raise ValueError(
                "Image dimensions not found in response parameters. "
                "Ensure the OIP adapter preserves request parameters in the response."
            )

        bbox_tensor = outputs[self.bbox_output_name]
        bboxes = self._extract_bboxes(bbox_tensor)
        labels = self._extract_tensor_data(outputs[self.label_output_name])
        scores = self._extract_tensor_data(outputs[self.score_output_name])

        # Validate all tensors have same length
        validate_tensor_lengths_match(
            bboxes, labels, scores, names=["bboxes", "labels", "scores"]
        )

        detections = []
        for bbox, label, score in zip(bboxes, labels, scores):
            detection = Detection(
                bbox=BoundingBox(
                    x1=float(bbox[0]),
                    y1=float(bbox[1]),
                    x2=float(bbox[2]),
                    y2=float(bbox[3]),
                ),
                label=str(label),
                confidence=float(score),
            )
            detections.append(detection)

        return ObjectDetectionResult(
            detections=detections,
            image_width=image_width,
            image_height=image_height,
        )

    def _extract_bboxes(self, tensor: TensorData) -> list[list[float]]:
        """Extract bounding boxes from tensor, reshaping if necessary.

        OIP may flatten [N, 4] tensor data into a flat list. This method
        reconstructs the bounding box structure based on the tensor shape.

        Args:
            tensor: TensorData with bounding box data

        Returns:
            List of [x1, y1, x2, y2] coordinate lists
        """
        data = self._extract_tensor_data(tensor)
        if not data:
            return []

        if isinstance(data[0], list):
            return data

        shape = tensor.shape
        if len(shape) == 2 and shape[1] == 4:
            num_boxes = shape[0]
            return [data[i * 4 : (i + 1) * 4] for i in range(num_boxes)]

        return data

    def _extract_tensor_data(self, tensor: TensorData) -> list[Any]:
        """Extract the actual data from a tensor, flattening if necessary.

        Args:
            tensor: TensorData object

        Returns:
            Flattened list of tensor values
        """
        data = tensor.data
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
            return data[0]
        return data
