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
from dataclasses import dataclass
from typing import Any


@dataclass
class BoundingBox:
    """Represents a bounding box for object detection.

    Attributes:
        x1: Left x-coordinate
        y1: Top y-coordinate
        x2: Right x-coordinate
        y2: Bottom y-coordinate
    """

    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def width(self) -> float:
        """Calculate the width of the bounding box."""
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        """Calculate the height of the bounding box."""
        return self.y2 - self.y1

    @property
    def area(self) -> float:
        """Calculate the area of the bounding box."""
        return self.width * self.height

    @property
    def center(self) -> tuple[float, float]:
        """Calculate the center point of the bounding box."""
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)


@dataclass
class Detection:
    """Represents a single detected object.

    Attributes:
        bbox: Bounding box coordinates
        label: Class label of the detected object
        confidence: Confidence score (0-1)
        label_id: Optional numeric ID for the label
    """

    bbox: BoundingBox
    label: str
    confidence: float
    label_id: int | None = None


@dataclass
class ObjectDetectionResult:
    """Value object representing the result of an object detection inference.

    Attributes:
        detections: List of detected objects
        image_width: Width of the input image
        image_height: Height of the input image
    """

    detections: list[Detection]
    image_width: int
    image_height: int

    def filter_by_confidence(self, threshold: float) -> "ObjectDetectionResult":
        """Filter detections by confidence threshold.

        Args:
            threshold: Minimum confidence score (0-1)

        Returns:
            New ObjectDetectionResult with filtered detections
        """
        filtered = [d for d in self.detections if d.confidence >= threshold]
        return ObjectDetectionResult(
            detections=filtered,
            image_width=self.image_width,
            image_height=self.image_height,
        )

    def filter_by_label(self, labels: list[str]) -> "ObjectDetectionResult":
        """Filter detections by label.

        Args:
            labels: List of labels to keep

        Returns:
            New ObjectDetectionResult with filtered detections
        """
        filtered = [d for d in self.detections if d.label in labels]
        return ObjectDetectionResult(
            detections=filtered,
            image_width=self.image_width,
            image_height=self.image_height,
        )

    def draw_on_image(self, image: Any) -> Any:
        """Draw bounding boxes on the image.

        Args:
            image: PIL Image or numpy array

        Returns:
            Image with drawn bounding boxes

        Raises:
            ImportError: If PIL is not installed
        """
        try:
            from PIL import Image, ImageDraw
        except ImportError as e:
            raise ImportError(
                "PIL (Pillow) is required for drawing. Install with: pip install Pillow"
            ) from e

        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)

        draw = ImageDraw.Draw(image)
        for detection in self.detections:
            bbox = detection.bbox
            draw.rectangle(
                [(bbox.x1, bbox.y1), (bbox.x2, bbox.y2)], outline="red", width=2
            )
            text = f"{detection.label}: {detection.confidence:.2f}"
            draw.text((bbox.x1, bbox.y1 - 10), text, fill="red")

        return image
