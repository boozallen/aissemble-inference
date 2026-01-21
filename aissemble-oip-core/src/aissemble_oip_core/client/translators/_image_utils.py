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
"""Shared utilities for image preprocessing in translators."""

import base64
from io import BytesIO
from typing import Any


def encode_image_for_oip(input_data: Any) -> tuple[str, int, int]:
    """Encode image to base64 string for OIP transport.

    Accepts various input formats:
    - PIL Image
    - numpy array
    - file path (string)
    - bytes

    Args:
        input_data: Image in various formats

    Returns:
        Tuple of (base64_string, width, height)

    Raises:
        ImportError: If PIL is not installed
        ValueError: If input type is not supported
    """
    try:
        from PIL import Image
    except ImportError as e:
        raise ImportError(
            "PIL (Pillow) is required for image handling. "
            "Install with: pip install Pillow"
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
