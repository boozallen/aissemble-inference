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
class OipRequest:
    """Placeholder class for OipRequest. To be implemented later."""
    pass


class OipResponse:
    """Placeholder class for OipResponse. To be implemented later."""
    pass


class OipHealthStatus:
    """Placeholder class for OipHealthStatus. To be implemented later."""
    pass


class OipAdapter:
    """This is the sole class that interacts with OIP endpoints. It is stateless and can be mocked for client testing.
    Implements appropriate backoff, authentication, and metrics capturing.
    """

    def infer(self, request: OipRequest) -> OipRequest:
        """Performs inference using the provided OIP request.

        Args:
            request: The OipRequest object containing inference parameters.

        Returns:
            The OipResponse object (placeholder return type).
        """
        raise NotImplementedError