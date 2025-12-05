###
# #%L
# aiSSEMBLE::Open Inference Protocol::Examples::MLServer Iris Classifier
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
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Booz Allen Hamilton Inc.
"""
Iris Classifier MLServer Model

This demonstrates serving machine learning inference via MLServer through OIP-compliant endpoints.
"""

from mlserver import MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression


class IrisClassifier(MLModel):
    """
    A Logistic Regression classifier for the Iris dataset.

    Input: Array of shape (n_samples, 4) with features:
        - sepal length (cm)
        - sepal width (cm)
        - petal length (cm)
        - petal width (cm)

    Output: Predicted species (0=setosa, 1=versicolor, 2=virginica)
            and class probabilities.
    """

    async def load(self) -> bool:
        """
        Load and train the model on the Iris dataset.
        """

        iris = load_iris()

        self.model = LogisticRegression(max_iter=200)
        self.model.fit(iris.data, iris.target)

        self.ready = True
        print(
            f"IrisClassifier '{self.name}' loaded - trained on {len(iris.data)} samples"
        )
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """
        Predict iris species from flower measurements.

        Args:
            payload: InferenceRequest with input array of shape (n_samples, 4)

        Returns:
            InferenceResponse with:
                - predictions: class indices (0, 1, or 2)
                - probabilities: confidence scores for each class
        """
        # Decode input array
        input_data = NumpyCodec.decode_input(payload.inputs[0])

        # Ensure 2D array
        if input_data.ndim == 1:
            input_data = input_data.reshape(1, -1)

        # Get predictions and probabilities
        predictions = self.model.predict(input_data)
        probabilities = self.model.predict_proba(input_data)

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[
                ResponseOutput(
                    name="predictions",
                    shape=list(predictions.shape),
                    datatype="INT64",
                    data=predictions.tolist(),
                ),
                ResponseOutput(
                    name="probabilities",
                    shape=list(probabilities.shape),
                    datatype="FP64",
                    data=probabilities.flatten().tolist(),
                ),
            ],
        )
