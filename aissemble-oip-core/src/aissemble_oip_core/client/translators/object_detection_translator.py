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
import base64
from io import BytesIO
from typing import Any

from aissemble_oip_core.client.oip_adapter import OipRequest, OipResponse, TensorData
from aissemble_oip_core.client.results import (
    BoundingBox,
    Detection,
    ObjectDetectionResult,
)
from aissemble_oip_core.client.translator import Translator


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
        self._image_width: int = 0
        self._image_height: int = 0

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
            OipRequest with encoded image tensor
        """
        image_bytes, width, height = self._encode_image(input_data)
        self._image_width = width
        self._image_height = height

        tensor = TensorData(
            name=self.input_name,
            shape=[1, len(image_bytes)],
            datatype="BYTES",
            data=[[image_bytes]],
        )

        return OipRequest(inputs=[tensor])

    def postprocess(self, response: OipResponse) -> ObjectDetectionResult:
        """Postprocess OipResponse into ObjectDetectionResult.

        Args:
            response: OIP response containing detection outputs

        Returns:
            ObjectDetectionResult with parsed detections
        """
        outputs = {out.name: out for out in response.outputs}

        bboxes = self._extract_tensor_data(outputs[self.bbox_output_name])
        labels = self._extract_tensor_data(outputs[self.label_output_name])
        scores = self._extract_tensor_data(outputs[self.score_output_name])

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
            image_width=self._image_width,
            image_height=self._image_height,
        )

    def _encode_image(self, input_data: Any) -> tuple[str, int, int]:
        """Encode image to base64 string for OIP transport.

        Args:
            input_data: Image in various formats

        Returns:
            Tuple of (base64_string, width, height)
        """
        try:
            from PIL import Image
        except ImportError as e:
            raise ImportError(
                "PIL (Pillow) is required for image handling. Install with: pip install Pillow"
            ) from e

        if isinstance(input_data, str):
            image = Image.open(input_data)
        elif isinstance(input_data, bytes):
            image = Image.open(BytesIO(input_data))
        elif hasattr(input_data, "mode"):
            image = input_data
        else:
            import numpy as np

            if isinstance(input_data, np.ndarray):
                image = Image.fromarray(input_data)
            else:
                raise ValueError(f"Unsupported input type: {type(input_data)}")

        width, height = image.size

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        encoded = base64.b64encode(image_bytes).decode("utf-8")

        return encoded, width, height

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
