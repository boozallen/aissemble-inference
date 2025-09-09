###
# #%L
# aiSSEMBLE::Open Inference Protocol::KServe
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from typing import Dict, Union, Optional, Tuple

from kserve import InferRequest, InferResponse, ModelRepository
from kserve.protocol.dataplane import DataPlane


class KServeDataplaneHandler(DataPlane):
    """KServe Custom DataPlane Handler"""

    def __init__(self):
        super().__init__(model_registry=ModelRepository())

    async def live(self) -> Dict[str, str]:
        """Server live
        Should return ``{"status": "alive"}`` on successful Server Live Check.
        """
        return {"status": "alive"}

    async def ready(self) -> bool:
        """Server ready
        Should return True on successful Server Ready Check.
        """
        return True

    def metadata(self) -> Dict:
        """Server Metadata
        Returns a dictionary with following fields:
           - name (str): name of the server.
           - version (str): server version number.
           - extension (list[str]): list of extensions supported by this server
        """
        return {
            "name": self._server_name,
            "version": self._server_version,
            "extensions": ["extensions"],
        }

    async def model_metadata(self, model_name: str) -> Dict:
        """Model Metadata
        Returns a dictionary with following fields:
                - name (str): name of the model
                - platform: "" (Empty String)
                - inputs: Dict with below fields
                    - name (str): name of the input
                    - datatype (str): Eg. INT32, FP32
                    - shape ([]int): The shape of the tensor.
                                   Variable-size dimensions are specified as -1.
                - outputs: Same as inputs described above.
        NOTE: Model Version is not supported yet in KServe.
        """

        return {
            "name": model_name,
            "platform": "",
            "inputs": [
                {
                    "name": "input",
                    "datatype": "INT32",
                    "shape": [1],
                }
            ],
            "outputs": [
                {
                    "name": "output",
                    "datatype": "INT32",
                    "shape": [1],
                }
            ],
        }

    async def model_ready(
        self, model_name: str, disable_predictor_health_check: bool = False
    ) -> bool:
        """Model Ready
        Should return True on successful Model Ready Check.
        """
        return True

    async def infer(
        self,
        model_name: str,
        request: Union[Dict, InferRequest],
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[Union[Dict, InferResponse], Dict[str, str]]:
        """Inference endpoint
        Performs inference on the specified model with the provided body and headers:

         Args:
            model_name (str): Model name.
            request (Dict | InferRequest): Request body data.
            headers: (Optional[Dict[str, str]]): Request headers.

        Returns:
            Tuple[Union[Dict, InferResponse], Dict[str, str]]:
                - response: The inference result.
                - response_headers: Headers to construct the HTTP response.

        """
        infer_response = InferResponse(
            response_id="", model_name=model_name, infer_outputs=[]
        )
        response_headers = {}
        return infer_response, response_headers

    def model_load(self, model_name: str) -> bool:
        pass
