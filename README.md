# aiSSEMBLE&trade; Open Inference Protocol

![PyPI - Version](https://img.shields.io/pypi/v/aissemble-open-inference-protocol-shared)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aissemble-open-inference-protocol-shared)
![PyPI - Format](https://img.shields.io/pypi/format/aissemble-open-inference-protocol-shared)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aissemble-open-inference-protocol-shared)
[![Build (github)](https://github.com/boozallen/aissemble-open-inference-protocol/actions/workflows/build.yaml/badge.svg)](https://github.com/boozallen/aissemble-open-inference-protocol/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/boozallen/aissemble-open-inference-protocol)](https://www.apache.org/licenses/LICENSE-2.0)

This repository provides a reference implementation of the [Open Inference Protocol (OIP)](https://github.com/kserve/open-inference-protocol) — a standard designed 
to promote interoperability across diverse inference runtimes and platforms. By adhering to a consistent API 
specification, OIP simplifies the integration and deployment of machine learning models in both development 
and production environments.

By integrating with aiSSEMBLE Open Inference Protocol, you get a practical, ready-to-use implementation of the OIP standard that streamlines the process of making your models interoperable. It abstracts away much of the complexity involved in conforming to the protocol, allowing you to easily connect with any OIP-compliant client or server. This enhances portability and ensures your models can run seamlessly across platforms that have adopted the OIP API.

## Current Platforms Supported:
  - [FastAPI](./aissemble-open-inference-protocol-fastapi/README.md#aissemble-open-inference-protocol-fastapi)
  - [gRPC](./aissemble-open-inference-protocol-grpc/README.md#aissemble-open-inference-protocol-grpc) 
  - [KServe](./aissemble-open-inference-protocol-kserve/README.md#aissemble-open-inference-protocol-kserve)

## Examples
aiSSEMBLE Open Inference Protocol provides a wide range of examples across different implementations and configurations. For the full list of examples, see the [Examples](./aissemble-open-inference-protocol-examples/README.md#aissemble-open-inference-protocol-examples) documentation.