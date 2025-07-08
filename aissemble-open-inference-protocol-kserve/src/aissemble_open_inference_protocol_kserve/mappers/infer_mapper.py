###
# #%L
# aiSSEMBLE::Open Inference Protocol::KServe
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###

from kserve import InferRequest, InferResponse, InferOutput

from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    RequestOutput,
    Datatype,
    TensorData,
)


class InferMapper:
    @staticmethod
    def infer_request_to_inference_request(request: InferRequest) -> InferenceRequest:
        inference_input_list = []
        inference_output_list = []
        # TODO Parameters need fix.
        for input in request.inputs:
            req_input = RequestInput(
                name=input.name,
                shape=input.shape,
                datatype=Datatype[input.datatype],
                parameters=input.parameters,
                data=TensorData(root=input.data),
            )
            inference_input_list.append(req_input)
        for output in request.request_outputs:
            req_output = RequestOutput(name=output.name, parameters=output.parameters)
            inference_output_list.append(req_output)
        return InferenceRequest(
            id=request.id,
            parameters=request.parameters,
            inputs=inference_input_list,
            outputs=inference_output_list,
        )

    @staticmethod
    def inference_response_to_infer_response(
        response: InferenceResponse,
    ) -> InferResponse:
        inference_list = []
        # TODO Parameters need fix.
        for output in response.outputs:
            res_output = InferOutput(
                name=output.name,
                shape=output.shape,
                datatype=output.datatype.value,
                parameters=output.parameters,
                data=output.data.root,
            )
            inference_list.append(res_output)
        return InferResponse(
            response_id=response.id,
            model_name=response.model_name,
            model_version=response.model_version,
            parameters=response.parameters,
            infer_outputs=inference_list,
            from_grpc=False,
        )
