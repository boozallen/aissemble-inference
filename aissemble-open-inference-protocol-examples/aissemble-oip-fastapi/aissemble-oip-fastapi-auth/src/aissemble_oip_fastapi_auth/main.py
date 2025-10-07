###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::FastAPI with Auth
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
import os
from typing import Optional

from fastapi import APIRouter, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
    AissembleOIPFastAPI,
)

# To enable authorization in your own project you should import AuthzforceAdapter
from aissemble_open_inference_protocol_shared.auth.authzforce_adapter import (
    AuthzforceAdapter,
)
from aissemble_open_inference_protocol_shared.handlers.model_handler import ModelHandler
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
)
from .generate_simple_jwt import (
    create_simple_jwt_token,
)

security = HTTPBearer(auto_error=False)
AUTH_ACTION_READ = "read"
AUTH_RESOURCE_DATA = "data"

routerWithSecurity = APIRouter(
    prefix="/v2",
    responses={404: {"description": "Not found"}},
)

"""
In your own project you will need to specify your Authzforce PDP url in 
the oip.properties file by changing pdp_url=<your url goes here> to point 
to your own server. In this example it is set to pdp_url=http://localhost:8080/pdp, 
which is the local url.
"""


class Handler(ModelHandler):
    def __init__(self):
        super().__init__()

    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        return InferenceResponse(
            model_name=model_name, model_version=model_version, id="id", outputs=[]
        )

    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        return ModelMetadataResponse(
            name=model_name,
            versions=["123"],
            platform="placeholder_platform",
            inputs=[],
            outputs=[],
        )

    def model_load(self, model_name: str) -> bool:
        # Stubbing any response because example does not have a model to load
        return True


class LoginRequest(BaseModel):
    username: str
    password: str


@routerWithSecurity.post(
    "/login",
    summary="Perform Authentication",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
def auth_login(
    payload: LoginRequest,
) -> dict:
    """
    Simulates a login.  This would typically be delegated to an IdP, which is not part of aiSSEMBLE OIP.
    """
    jwt_token = create_simple_jwt_token({"sub": payload.username})
    return {"jwt": jwt_token}


# Set the Krausening configuration path so the properties will be picked up. This is assuming the script is being run
# locally and would fail for dockerized deployments. This is only to ease running the example
os.environ["KRAUSENING_BASE"] = os.getcwd() + "/src/resources/krausening/base/"

# To enable authorization in your own project you need to inject AuthzforceAdapter
# into your app like the example below
server = AissembleOIPFastAPI(Handler(), AuthzforceAdapter()).server
server.include_router(routerWithSecurity)
