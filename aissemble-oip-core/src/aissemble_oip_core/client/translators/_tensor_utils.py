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
"""Shared utilities for tensor validation and extraction."""

from typing import Any

from aissemble_oip_core.client.oip_adapter import TensorData


def validate_required_tensors(
    outputs: dict[str, TensorData], required: list[str], format_name: str
) -> None:
    """Validate that all required tensors are present in outputs.

    Args:
        outputs: Dictionary mapping tensor names to TensorData
        required: List of required tensor names
        format_name: Name of the format for error messages (e.g., "TensorFlow")

    Raises:
        ValueError: If any required tensors are missing
    """
    missing = [name for name in required if name not in outputs]
    if missing:
        raise ValueError(
            f"{format_name} format requires tensors {missing} but server returned: "
            f"{list(outputs.keys())}"
        )


def validate_tensor_lengths_match(
    *tensors: list[Any], names: list[str] | None = None
) -> None:
    """Validate that all tensors have the same length.

    Args:
        *tensors: Variable number of tensor data lists
        names: Optional names for error messages

    Raises:
        ValueError: If tensor lengths don't match
    """
    lengths = [len(t) for t in tensors]
    if len(set(lengths)) > 1:
        if names:
            details = ", ".join(f"{len(t)} {name}" for t, name in zip(tensors, names))
            raise ValueError(f"Tensor length mismatch: {details}. Expected all equal.")
        else:
            raise ValueError(f"Tensor length mismatch: {lengths}. Expected all equal.")


def unbatch_tensor(tensor: TensorData, num_items: int | None = None) -> list[Any]:
    """Extract data from batched tensor [1, N, ...] -> [N, ...] and apply limit.

    Args:
        tensor: TensorData with potentially batched data
        num_items: Optional limit on number of items to extract

    Returns:
        Unbatched list of items
    """
    data = tensor.data

    # Unbatch if [1, N] or [1, N, M] shape
    if isinstance(data, list) and data and isinstance(data[0], list):
        data = data[0]

    # Apply limit if specified
    if num_items is not None:
        data = data[:num_items]

    return data
