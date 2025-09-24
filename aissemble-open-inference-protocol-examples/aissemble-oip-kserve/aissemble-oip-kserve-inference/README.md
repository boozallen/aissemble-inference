[[Return to Examples Documentation]](../../README.md)

# aiSSEMBLE&trade; Open Inference Protocol KServe Getting Started Example
This example provides simple guideline on how to hook the model logic into KServe to implement its inference endpoint.

## Getting Started
* This is intended for users who have already set up the base infrastructure (CRD, KServe, ingress, cert-manager) and want to hook up a model using aiSSEMBLE Open Inference Protocol for KServe.
* KServe Infrastructure setup should be completed per KServe [Documentation](https://kserve.github.io/website/docs/admin-guide/kubernetes-deployment)

## Implementation of Custom Predictor for KServe
- The example will employ simple keras tensorflow model file as a model. 
- This only covers how the model logic can interact with KServe
- [main.py](src/aissemble_oip_kserve_inference/main.py) describes how to pull `AissembleOIPKServe` handler and start the KServe Model Server.
- `AissembleOIPKServe` is KServeHandler class for aiSSEMBLE Open Inference Protocol, in which user can instantiate and start the model server.
- preprocess() and postprocess() are also implemented to demonstrate user have option to override those two methods and 
- If user wants to create Custom Predictor for their need, user can also extend `AissembleOIPKServe` handler class and implement custom logic.
- For `DataplaneHandler`, user should be implementing their own implementation of OIP handler based on `DataplaneHandler` abstract base class.
