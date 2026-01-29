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
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from aissemble_inference_core.client.oip_adapter import OipRequest, OipResponse

I = TypeVar("I")
O = TypeVar("O")


class Translator(ABC, Generic[I, O]):
    """
    Directly inspired by DJL, this is the ONLY class that knows about the OIP json schema,
    tensor shapes, inputs, parameters, framing, etc. It is intended to be pluggable and
    testable in isolation. It also provides tolerable reader behavior, where unknown
    fields can be ignored.
    """

    @abstractmethod
    def preprocess(self, input: I) -> OipRequest:
        """
        Preprocesses the input to create an OipRequest.

        :param input: The input data of type I.
        :return: An OipRequest object.
        """
        # TODO: Implement OipRequest creation
        pass

    @abstractmethod
    def postprocess(self, response: OipResponse) -> O:
        """
        Postprocesses the OipResponse to produce the output.

        :param response: The OipResponse object.
        :return: The output data of type O.
        """
        # TODO: Implement OipResponse creation
        pass
