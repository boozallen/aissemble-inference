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
"""YOLO-specific translator for object detection.

This module provides a translator optimized for YOLO model outputs.
Currently uses the default object detection translator from core,
but can be extended with YOLO-specific optimizations if needed.
"""

from aissemble_inference_core.client.translators import DefaultObjectDetectionTranslator


class YOLOTranslator(DefaultObjectDetectionTranslator):
    """Translator for YOLO object detection models.

    This translator handles the standard YOLO output format:
    - bboxes: [N, 4] tensor with coordinates (x1, y1, x2, y2)
    - labels: [N] tensor with class names
    - scores: [N] tensor with confidence scores

    Currently inherits all behavior from DefaultObjectDetectionTranslator.
    Can be extended with YOLO-specific preprocessing or postprocessing
    if needed (e.g., NMS configuration, class filtering).
    """

    pass
