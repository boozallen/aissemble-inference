[[Return to Examples Documentation]](../../README.md)

# aiSSEMBLE Open Inference Protocol&trade; KServe Inference Example
This example provides simple guideline on how to hook model into aiSSEMBLE Open Interface Protocol FastAPI and use KServe to implement inference endpoint.


## Getting Started
* This is intended for users who have already set up the base infrastructure (CRD, KServe, ingress, cert-manager) and want to hook up a model using aiSSEMBLE Open Inference Protocol Handler for KServe.
* KServe Infrastructure setup should be completed per KServe [Documentation](https://kserve.github.io/website/master/admin/kubernetes_deployment/)

## Implementation of Custom Predictor for KServe
- The example will employ simple keras tensorflow model file as a model. 
- This only covers how handler can interact with KServe
- [main.py](./src/aissemble-oip-kserve-inference/main.py) describes how to pull `AissembleOIPKServe` handler and start the KServe Model Server.
- `AissembleOIPKServe` is KserveHandler class for aiSSEMBLE Open Inference Protocol, in which user can instantiate and start the model server.
- If user wants to create Custom Predictor for their need, user can also extend `AissembleOIPKServe` handler class and implement custom logic.
- For `DataplaneHandler`, user should be implementing their own implementation of OIP handler based on `DataplaneHandler` abstract base class.