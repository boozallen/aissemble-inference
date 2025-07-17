# aiSSEMBLE Open Inference Protocol KServe Example
This example provides simple guideline on how to hook model into Aissemble Open Interface Protocol FastAPI and use KServe to implement inference endpoint.


## Prerequisites
* This is intended for users who already have set up base infrastructures (CRD, KServe, ingress, cert-manager) and want to hook model using Aissemble Open Inference Protocol Handler for Kserve.
* Kserve Infrastructure setup should be completed per KServe [Documentation](https://kserve.github.io/website/master/admin/kubernetes_deployment/)

## Implementation of custom predictor for KServe
- The example will employ simple keras tensorflow model file as a model. 
- This only covers how handler can interact with Kserve
- [main.py](./src/aissemble-oip-kserve-inference/main.py) describes how to pull AissembleOIPKServe handler and start the Kserve Model Server.
- AissembleOIPKServe is KserveHandler class for Aissemble OIP, in which user can instantiate and start the model server.
- If user wants to create Custom Predictor for their need, user can also extend AissembleOIPKServe handler class and implement custom logic.
- For DataplaneHandler, user should be implementing their own implementation of OIP handler based on DataplaneHandler abstract base class.