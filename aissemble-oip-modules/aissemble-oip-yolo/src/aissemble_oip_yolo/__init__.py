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
"""aiSSEMBLE OIP YOLO Module.

This module provides YOLO model family support for the aiSSEMBLE
Open Inference Protocol library.

Supported YOLO versions (via Ultralytics):
- YOLOv5: yolov5n, yolov5s, yolov5m, yolov5l, yolov5x
- YOLOv8: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
- YOLO11: yolo11n, yolo11s, yolo11m, yolo11l, yolo11x

Usage:
    # Install the module
    pip install aissemble-oip-yolo

    # The module registers itself via entry points
    # InferenceClient will automatically discover it

Example MLServer configuration (model-settings.json):
    {
        "name": "yolo",
        "implementation": "aissemble_oip_yolo.YOLORuntime",
        "parameters": {
            "model": "yolov8n.pt"
        }
    }
"""

from aissemble_oip_yolo.runtime import YOLORuntime
from aissemble_oip_yolo.translator import YOLOTranslator

__all__ = ["YOLORuntime", "YOLOTranslator"]
