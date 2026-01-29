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
"""TensorFlow Object Detection API translator for OIP object detection.

This translator handles the TensorFlow Object Detection API / TensorFlow Serving
tensor format, commonly used with models exported from TensorFlow Model Zoo.

Key format characteristics:
- Normalized coordinates [0, 1] instead of pixel coordinates
- TensorFlow Serving-style tensor names (detection_boxes, detection_classes, etc.)
- Batched shape conventions [1, N, 4] instead of [N, 4]
- Integer class IDs requiring mapping to label names
- Coordinate order: (ymin, xmin, ymax, xmax) instead of (x1, y1, x2, y2)

Despite these differences from the default YOLO-style format, end users use the
SAME client API - the translator handles all tensor-level complexity invisibly.

Thread Safety:
This translator is thread-safe and stateless. Image dimensions are stored in
request parameters and retrieved from response parameters.
"""

import logging
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
    unbatch_tensor,
    validate_required_tensors,
    validate_tensor_lengths_match,
)

logger = logging.getLogger(__name__)


class TensorFlowObjectDetectionTranslator(Translator[Any, ObjectDetectionResult]):
    """Translator for TensorFlow Object Detection API / TensorFlow Serving format.

    This translator handles the standard TensorFlow Object Detection API output format,
    commonly used by models exported from TensorFlow Model Zoo and served via TensorFlow
    Serving, KServe, or other TF-compatible inference backends.

    Expected output tensors:
    - detection_boxes: [1, N, 4] with NORMALIZED coordinates (ymin, xmin, ymax, xmax)
    - detection_classes: [1, N] with integer class IDs
    - detection_scores: [1, N] with confidence scores
    - num_detections: [1] with count of valid detections

    Key differences from default YOLO-style format:
    1. Normalized coords [0,1] vs pixel coords
    2. Different coord order: (ymin, xmin, ymax, xmax) vs (x1, y1, x2, y2)
    3. Batched shape [1, N, 4] vs unbatched [N, 4]
    4. Integer class IDs vs string labels
    5. Extra num_detections tensor

    Despite these differences, users interact with the same ObjectDetectionResult
    type, demonstrating complete tensor abstraction.
    """

    def __init__(
        self,
        class_names: dict[int, str] | None = None,
    ):
        """Initialize translator with class ID to name mapping.

        Args:
            class_names: Optional mapping of class IDs to human-readable names.
                        If None, uses class IDs as labels (e.g., "class_17").
        """
        self._class_names = class_names or {}

    def preprocess(self, input_data: Any) -> OipRequest:
        """Preprocess image input into OipRequest.

        Accepts PIL Image, numpy array, file path, or bytes.

        Args:
            input_data: Image data in supported format

        Returns:
            OipRequest with encoded image tensor and dimensions in parameters
        """
        image_bytes, width, height = encode_image_for_oip(input_data)

        tensor = TensorData(
            name="image",
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

        Handles the TensorFlow Object Detection API tensor format:
        - Validates required tensors are present
        - Extracts batch dimension [1, N, ...] -> [N, ...]
        - Converts normalized coords to pixel coords
        - Reorders coords from (ymin, xmin, ymax, xmax) to (x1, y1, x2, y2)
        - Maps class IDs to names
        - Respects num_detections count

        Args:
            response: OIP response with TensorFlow format tensors and dimensions

        Returns:
            ObjectDetectionResult - same as default translator!

        Raises:
            ValueError: If required tensors are missing or malformed
        """
        outputs = {out.name: out for out in response.outputs}

        # Validate required tensors are present
        required = ["detection_boxes", "detection_classes", "detection_scores"]
        validate_required_tensors(outputs, required, "TensorFlow Object Detection API")

        # Get image dimensions from response parameters
        params = response.parameters or {}
        image_width = params.get("_image_width")
        image_height = params.get("_image_height")

        if image_width is None or image_height is None:
            raise ValueError(
                "Image dimensions not found in response parameters. "
                "Ensure the OIP adapter preserves request parameters in the response."
            )

        # Extract num_detections if present, otherwise use all detections
        num_detections = self._get_num_detections(outputs)

        # Extract and unbatch tensors [1, N] -> [N]
        boxes = unbatch_tensor(outputs["detection_boxes"], num_detections)
        class_ids = [
            int(cid)
            for cid in unbatch_tensor(outputs["detection_classes"], num_detections)
        ]
        scores = [
            float(s)
            for s in unbatch_tensor(outputs["detection_scores"], num_detections)
        ]

        # Validate all tensors have same length
        validate_tensor_lengths_match(
            boxes, class_ids, scores, names=["boxes", "classes", "scores"]
        )

        detections = []
        for box, class_id, score in zip(boxes, class_ids, scores):
            # Validate normalized coordinate range
            ymin_norm, xmin_norm, ymax_norm, xmax_norm = box
            if not all(0 <= coord <= 1 for coord in box):
                logger.warning(
                    f"Normalized coordinates outside [0,1] range: {box}. "
                    f"Server may be misconfigured or model may be wrong type."
                )

            # Convert normalized coords to pixel coords and reorder
            x1 = xmin_norm * image_width
            y1 = ymin_norm * image_height
            x2 = xmax_norm * image_width
            y2 = ymax_norm * image_height

            # Map class ID to name
            label = self._class_names.get(class_id, f"class_{class_id}")

            detection = Detection(
                bbox=BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2),
                label=label,
                confidence=score,
            )
            detections.append(detection)

        return ObjectDetectionResult(
            detections=detections,
            image_width=image_width,
            image_height=image_height,
        )

    def _get_num_detections(self, outputs: dict[str, TensorData]) -> int | None:
        """Extract number of valid detections from num_detections tensor if present.

        Args:
            outputs: Dictionary of output tensors

        Returns:
            Number of detections or None if tensor not present
        """
        if "num_detections" not in outputs:
            return None

        num_det_data = outputs["num_detections"].data
        if isinstance(num_det_data, list):
            return int(num_det_data[0]) if num_det_data else None
        return int(num_det_data)
