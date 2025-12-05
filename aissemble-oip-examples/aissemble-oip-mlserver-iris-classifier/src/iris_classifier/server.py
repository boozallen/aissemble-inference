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
"""MLServer launcher"""

import asyncio

from mlserver.settings import Settings, ModelSettings, ModelParameters
from mlserver.server import MLServer

from iris_classifier.model import IrisClassifier


async def main():
    settings = Settings(
        debug=True,
        parallel_workers=0,
    )

    model_settings = ModelSettings(
        name="iris-classifier",
        implementation=IrisClassifier,
        parameters=ModelParameters(version="v1.0.0"),
    )

    server = MLServer(settings)
    await server.start([model_settings])


def run_server():
    """Entry point for running the server via console script."""
    asyncio.run(main())


if __name__ == "__main__":
    run_server()
