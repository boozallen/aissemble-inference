###
# #%L
# aiSSEMBLE::Open Inference Protocol::Shared
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel
from pydantic import Field, RootModel, ConfigDict


class Parameters(BaseModel):
    content_type: Optional[str] = None
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={"additionalProperties": False},
    )


class TensorData(RootModel[Union[List, Any]]):
    root: Union[List, Any] = Field(..., title="TensorData")

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, idx):
        return self.root[idx]

    def __len__(self):
        return len(self.root)


class RequestOutput(BaseModel):
    name: str
    parameters: Optional[Parameters] = None


class Datatype(Enum):
    BOOL = "BOOL"
    UINT8 = "UINT8"
    UINT16 = "UINT16"
    UINT32 = "UINT32"
    UINT64 = "UINT64"
    INT8 = "INT8"
    INT16 = "INT16"
    INT32 = "INT32"
    INT64 = "INT64"
    FP16 = "FP16"
    FP32 = "FP32"
    FP64 = "FP64"
    BYTES = "BYTES"


class RequestInput(BaseModel):
    name: str
    shape: List[int]
    datatype: Datatype
    parameters: Optional[Parameters] = None
    data: TensorData


class ResponseOutput(BaseModel):
    name: str
    shape: List[int]
    datatype: Datatype
    parameters: Optional[Parameters] = None
    data: TensorData


class InferenceResponse(BaseModel):
    model_name: str
    model_version: Optional[str] = None
    id: Optional[str] = None
    parameters: Optional[Parameters] = None
    outputs: List[ResponseOutput]


class InferenceRequest(BaseModel):
    id: Optional[str] = None
    parameters: Optional[Parameters] = None
    inputs: List[RequestInput]
    outputs: Optional[List[RequestOutput]] = None


class MetadataTensor(BaseModel):
    name: str
    datatype: Datatype
    shape: List[int]


class ModelMetadataResponse(BaseModel):
    name: str
    versions: Optional[List[str]] = None
    platform: str
    inputs: List[MetadataTensor]
    outputs: List[MetadataTensor]


class ModelMetadataErrorResponse(BaseModel):
    error: str


class ModelReadyResponse(BaseModel):
    name: str
    ready: bool


class ServerReadyResponse(BaseModel):
    live: bool


class ServerLiveResponse(BaseModel):
    live: bool


class ServerMetadataResponse(BaseModel):
    name: str
    version: str
    extensions: List[str]


class ServerMetadataErrorResponse(BaseModel):
    error: str
