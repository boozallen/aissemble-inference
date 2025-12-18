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
from __future__ import annotations

from typing import Generic, TypeVar

# Input type variable - represents the type of data fed into the model for inference
T = TypeVar("T")

# Output type variable - represents the type of prediction/result returned by the model
R = TypeVar("R")


class Predictor(Generic[T, R]):
    """
    An interface representing a ready-to-use inference wrapper around a specific model endpoint.

    Inspired by the DJL (Deep Java Library) ``Predictor`` abstraction, this interface defines a
    lightweight, reusable component that encapsulates the invocation of a model while managing
    underlying resources such as connection pools, retries, timeouts, and authentication.

    Implementations are expected to be thread-safe where appropriate and should maintain internal
    state (e.g., HTTP clients, gRPC channels, or cached credentials) for efficient repeated use.
    Typically, one ``Predictor`` instance is created per model endpoint/version and reused across
    multiple inference calls.

    Example usage::

        predictor: Predictor[Image, Classification] = model.new_predictor()
        result = predictor.predict(my_image)

    """

    def predict(self, input: T) -> R:  # noqa: A003
        """
        Perform inference on the given input and return the model's prediction.

        Parameters
        ----------
        input : T
            The input data in the format expected by the wrapped model. The exact type depends
            on the model (e.g., ``numpy.ndarray``, ``PIL.Image.Image``, ``dict[str, Any]``, etc.).

        Returns
        -------
        R
            The prediction result. The concrete return type is determined by the model's output
            schema (e.g., ``Classification``, ``List[float]``, ``dict[str, Any]``, etc.).

        Raises
        ------
        InferenceError
            If the inference request fails after retries are exhausted or due to an unrecoverable
            error (e.g., malformed input, model endpoint unreachable, timeout).
        ValueError
            If the input does not conform to the expected schema or constraints.
        """
        raise NotImplementedError("Subclasses must implement predict()")
