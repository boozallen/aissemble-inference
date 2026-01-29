###
# #%L
# aiSSEMBLE::Open Inference Protocol::Modules::YOLO
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
"""YOLO model family runtime for MLServer.

This module provides an MLServer-compatible runtime that wraps YOLO models
(YOLOv5, YOLOv8, YOLO11, etc.) for object detection inference via the
Open Inference Protocol.
"""

import base64
from io import BytesIO

from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput
from PIL import Image


class YOLORuntime(MLModel):
    """MLServer runtime for YOLO object detection models.

    Supports multiple YOLO versions through the Ultralytics library:
    - YOLOv5: yolov5n, yolov5s, yolov5m, yolov5l, yolov5x
    - YOLOv8: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
    - YOLO11: yolo11n, yolo11s, yolo11m, yolo11l, yolo11x

    Configuration via model-settings.json:
        {
            "name": "yolo",
            "implementation": "aissemble_inference_yolo.YOLORuntime",
            "parameters": {
                "model": "yolov8n.pt"
            }
        }

    This runtime accepts base64-encoded images and returns:
    - bboxes: Bounding box coordinates [x1, y1, x2, y2]
    - labels: Class labels for each detection
    - scores: Confidence scores for each detection
    """

    async def load(self) -> bool:
        """Load the YOLO model.

        The model variant is specified via the 'model' parameter in
        model-settings.json. Defaults to 'yolov8n.pt' if not specified.

        Returns:
            True if model loaded successfully
        """
        from ultralytics import YOLO

        model_variant = self._get_model_variant()
        self._model = YOLO(model_variant)
        self.ready = True
        return self.ready

    async def health(self) -> dict:
        """Health check endpoint.

        Returns a lightweight health status without running expensive inference.
        This is called by MLServer's `/v2/health/ready` endpoint.

        Returns:
            Health status dict
        """
        return {"status": "ok"}

    def _get_model_variant(self) -> str:
        """Get the model variant from settings.

        Supports both direct attribute access (for backwards compatibility)
        and extra dict access (MLServer 1.6+ style).

        Returns:
            Model variant string, defaults to 'yolov8n.pt'
        """
        default = "yolov8n.pt"
        params = self.settings.parameters
        if params is None:
            return default

        # Try direct attribute access first (backwards compatibility)
        if hasattr(params, "model") and params.model is not None:
            return params.model

        # Try extra dict (MLServer 1.6+ style)
        if hasattr(params, "extra") and params.extra:
            return params.extra.get("model", default)

        return default

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """Run object detection on the input image.

        Args:
            payload: OIP inference request with base64-encoded image

        Returns:
            OIP response with bboxes, labels, and scores

        Raises:
            ValueError: If payload is malformed or missing image data
        """
        if not payload.inputs or len(payload.inputs) == 0:
            raise ValueError("Payload must contain at least one input tensor")

        image_input = payload.inputs[0]
        if not image_input.data or len(image_input.data) == 0:
            raise ValueError(f"Input '{image_input.name}' must contain data")

        # Handle both nested [0][0] format and flat [0] format
        if isinstance(image_input.data[0], (list, tuple)):
            image_data = image_input.data[0][0]
        else:
            image_data = image_input.data[0]

        if image_data is None:
            raise ValueError("Image data cannot be None")

        if isinstance(image_data, str):
            image_bytes = base64.b64decode(image_data)
        else:
            image_bytes = image_data

        image = Image.open(BytesIO(image_bytes))

        results = self._model(image, verbose=False)
        result = results[0]

        boxes = result.boxes
        bboxes = boxes.xyxy.cpu().numpy().tolist() if len(boxes) > 0 else []
        scores = boxes.conf.cpu().numpy().tolist() if len(boxes) > 0 else []
        class_ids = boxes.cls.cpu().numpy().tolist() if len(boxes) > 0 else []

        labels = [result.names[int(cls_id)] for cls_id in class_ids]

        return InferenceResponse(
            model_name=self.name,
            outputs=[
                ResponseOutput(
                    name="bboxes",
                    shape=[len(bboxes), 4] if bboxes else [0, 4],
                    datatype="FP32",
                    data=bboxes,
                ),
                ResponseOutput(
                    name="labels",
                    shape=[len(labels)],
                    datatype="BYTES",
                    data=labels,
                ),
                ResponseOutput(
                    name="scores",
                    shape=[len(scores)],
                    datatype="FP32",
                    data=scores,
                ),
            ],
        )
