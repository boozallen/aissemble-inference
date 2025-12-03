# aiSSEMBLE&trade; Open Inference Protocol

![PyPI - Version](https://img.shields.io/pypi/v/aissemble-open-inference-protocol-shared)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aissemble-open-inference-protocol-shared)
![PyPI - Format](https://img.shields.io/pypi/format/aissemble-open-inference-protocol-shared)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aissemble-open-inference-protocol-shared)
[![Build (github)](https://github.com/boozallen/aissemble-open-inference-protocol/actions/workflows/build.yaml/badge.svg)](https://github.com/boozallen/aissemble-open-inference-protocol/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/boozallen/aissemble-open-inference-protocol)](https://www.apache.org/licenses/LICENSE-2.0)

**v1.5 – Early Preview**

The aiSSEMBLE [Open Inference Protocol (OIP)](https://github.com/kserve/open-inference-protocol) project is evolving 
from a reference implementation of the Open Inference Protocol into a **modular, enterprise-ready Python library** 
designed to help data science teams move ML models from prototype to secure, scalable production with minimal friction.

## High-Level Goals for v1.5

- Remain fully compliant with the Open Inference Protocol (OIP) specification  
- Provide a lightweight, extensible library built on MLServer as the core inference engine  
- Serve as production-grade “glue” between existing data science artifacts and enterprise deployment targets  
- Enable rapid, repeatable deployment to diverse environments (Kubernetes, AWS, on-prem, edge)  
- Offer pluggable integrations and sensible defaults for:  
  - Security (authentication, authorization, encryption)  
  - Observability (centralized logging, Prometheus/Grafana metrics)  
  - Compliance needs common in regulated settings (FedRAMP, NIST, DoD IL support)  
- Simplify handoffs across data scientists, software engineers, and DevSecOps teams via standardized, framework-agnostic 
 abstractions  

This version focuses on establishing the core architecture, extension points, and initial capabilities. Detailed 
documentation, examples, contribution guides, and full feature specifications will be expanded progressively as part 
of the v1.5 effort.

**Status:** Active development – not yet feature-complete.  
Feedback and early adopters welcome.