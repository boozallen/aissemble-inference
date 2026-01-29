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
from typing import Any, Generator

from aissemble_inference_core.client.builder.inference_builder import InferenceBuilder
from aissemble_inference_core.client.predictor import Predictor
from aissemble_inference_core.client.results import ObjectDetectionResult
from aissemble_inference_core.client.translators import DefaultObjectDetectionTranslator


class ObjectDetectionPredictor(Predictor[Any, ObjectDetectionResult]):
    """Concrete predictor implementation for object detection."""

    def __init__(
        self,
        adapter: Any,
        translator: DefaultObjectDetectionTranslator,
    ):
        """Initialize the object detection predictor.

        Args:
            adapter: OIP adapter for communication
            translator: Translator for preprocessing/postprocessing
        """
        self.adapter = adapter
        self.translator = translator

    def predict(self, input_data: Any) -> ObjectDetectionResult:  # noqa: A003
        """Perform object detection on the input image.

        Args:
            input_data: Image in various formats (PIL, numpy, path, bytes)

        Returns:
            ObjectDetectionResult with detected objects
        """
        request = self.translator.preprocess(input_data)
        response = self.adapter.infer(request)
        return self.translator.postprocess(response)


class ObjectDetectionBuilder(InferenceBuilder):
    """Task-specific builder for object detection inference.

    Provides a fluent, natural API for object detection:
        builder.image(my_image).confidence(0.5).run()

    Example:
        client = InferenceClient(adapter, endpoint)
        result = (client.detect_object()
                       .with_model("yolov8")
                       .image("photo.jpg")
                       .confidence(0.6)
                       .run())
    """

    def __init__(self):
        """Initialize the object detection builder."""
        super().__init__()
        self._image_input: Any = None
        self._confidence_threshold: float = 0.0
        self._filter_labels: list[str] | None = None

    def image(self, image: Any) -> "ObjectDetectionBuilder":
        """Set the input image for detection.

        Args:
            image: Image in various formats (PIL Image, numpy array, file path, bytes)

        Returns:
            Self for method chaining
        """
        self._image_input = image
        return self

    def confidence(self, threshold: float) -> "ObjectDetectionBuilder":
        """Set minimum confidence threshold for detections.

        Args:
            threshold: Minimum confidence score (0-1)

        Returns:
            Self for method chaining
        """
        if not 0 <= threshold <= 1:
            raise ValueError("Confidence threshold must be between 0 and 1")
        self._confidence_threshold = threshold
        return self

    def labels(self, labels: list[str]) -> "ObjectDetectionBuilder":
        """Filter detections to only include specified labels.

        Args:
            labels: List of labels to include

        Returns:
            Self for method chaining
        """
        self._filter_labels = labels
        return self

    def run(self) -> ObjectDetectionResult:
        """Execute the object detection inference.

        Returns:
            ObjectDetectionResult with detected objects

        Raises:
            ValueError: If required inputs are missing
        """
        if self._image_input is None:
            raise ValueError("Image input is required. Call .image() first.")

        predictor = self.build_predictor()
        result = predictor.predict(self._image_input)

        if self._confidence_threshold > 0:
            result = result.filter_by_confidence(self._confidence_threshold)

        if self._filter_labels:
            result = result.filter_by_label(self._filter_labels)

        return result

    def build_predictor(self) -> Predictor[Any, ObjectDetectionResult]:
        """Build the predictor for object detection.

        Returns:
            ObjectDetectionPredictor instance

        Raises:
            ValueError: If adapter or translator is not set
        """
        if self.oip_adapter is None:
            raise ValueError("OipAdapter is required. Call .with_adapter() first.")

        translator = (
            self.translator
            if isinstance(self.translator, DefaultObjectDetectionTranslator)
            else DefaultObjectDetectionTranslator()
        )

        return ObjectDetectionPredictor(
            adapter=self.oip_adapter,
            translator=translator,
        )

    def __iter__(self) -> Generator[ObjectDetectionResult, None, None]:
        """Streaming iteration for object detection.

        Not typically used for object detection but provided for consistency.

        Yields:
            ObjectDetectionResult instances
        """
        raise NotImplementedError(
            "Streaming is not supported for object detection tasks"
        )

    def __next__(self) -> ObjectDetectionResult:
        """Return the next streaming result.

        Not typically used for object detection but provided for Iterator protocol.

        Returns:
            ObjectDetectionResult instance

        Raises:
            NotImplementedError: Streaming is not supported for object detection
        """
        raise NotImplementedError(
            "Streaming is not supported for object detection tasks"
        )
