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
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #L%
###
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TensorData:
    """Represents tensor data in OIP format.

    Attributes:
        name: Name of the tensor input/output
        shape: Shape of the tensor as a list of integers
        datatype: Data type string (e.g., "FP32", "UINT8", "BYTES")
        data: The actual tensor data (nested list structure)
        parameters: Optional parameters for this tensor
    """

    name: str
    shape: list[int]
    datatype: str
    data: list[Any]
    parameters: dict[str, Any] | None = None


@dataclass
class OipRequest:
    """Represents an OIP inference request compliant with the Open Inference Protocol specification.

    Attributes:
        inputs: List of input tensors (required)
        id: Optional request identifier
        parameters: Optional inference parameters
        outputs: Optional list of requested output names
    """

    inputs: list[TensorData]
    id: str | None = None  # noqa: A003
    parameters: dict[str, Any] = field(default_factory=dict)
    outputs: list[dict[str, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert the request to a dictionary for JSON serialization."""
        result: dict[str, Any] = {
            "inputs": [
                {
                    "name": inp.name,
                    "shape": inp.shape,
                    "datatype": inp.datatype,
                    "data": inp.data,
                    **({"parameters": inp.parameters} if inp.parameters else {}),
                }
                for inp in self.inputs
            ]
        }
        if self.id:
            result["id"] = self.id
        if self.parameters:
            result["parameters"] = self.parameters
        if self.outputs:
            result["outputs"] = self.outputs
        return result


@dataclass
class OipResponse:
    """Represents an OIP inference response compliant with the Open Inference Protocol specification.

    Attributes:
        model_name: Name of the model that produced this response
        outputs: List of output tensors
        model_version: Optional version of the model
        id: Optional request identifier echo
        parameters: Optional response parameters
    """

    model_name: str
    outputs: list[TensorData]
    model_version: str | None = None
    id: str | None = None  # noqa: A003
    parameters: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OipResponse":
        """Create an OipResponse from a dictionary (JSON deserialization)."""
        outputs = [
            TensorData(
                name=out["name"],
                shape=out["shape"],
                datatype=out["datatype"],
                data=out["data"],
                parameters=out.get("parameters"),
            )
            for out in data["outputs"]
        ]
        return cls(
            model_name=data["model_name"],
            outputs=outputs,
            model_version=data.get("model_version"),
            id=data.get("id"),
            parameters=data.get("parameters"),
        )


@dataclass
class OipHealthStatus:
    """Represents the health status of an OIP endpoint.

    Attributes:
        isLive: Whether the endpoint is alive
        isReady: Whether the endpoint is ready to serve requests
    """

    isLive: bool
    isReady: bool


class OipAdapter:
    """This is the sole class that interacts with OIP endpoints. It is stateless and can be mocked for client testing.
    Implements appropriate backoff, authentication, and metrics capturing.
    """

    def infer(self, request: OipRequest) -> OipResponse:
        """Performs inference using the provided OIP request.

        Args:
            request: The OipRequest object containing inference parameters.

        Returns:
            The OipResponse object.
        """
        raise NotImplementedError
