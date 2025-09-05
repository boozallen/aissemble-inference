# aiSSEMBLE Open Inference Protocol&trade; KServe Containerization Example
This example demonstrates how to containerize the aiSSEMBLE Open Interface Protocol and deploy it on KServe


## Prerequisites
* This is intended for users who already have set up base infrastructures (CRD, KServe, ingress, cert-manager) and want to make use of docker containerization using [Habushu Containerization](https://github.com/TechnologyBrewery/habushu/blob/dev/examples/habushu-containerize/README.md) to deploy custom model to KServe.


## Getting Started
* This example will make use of [KServe Inference Example](../aissemble-oip-kserve-inference/README.md) to containerize and deploy aiSSEMBLE Open Interface Protocol to KServe 
* This example will cover REST and gRPC based API calls and will be deployed locally for demonstration purpose.
* This example consists of 2 modules:
  * `aissemble-oip-kserve-containerization-deploy`
    * This module contains list of helm template files needed to deploy custom model to KServe.
    * inference-service.yaml will take docker image created from aissemble-oip-kserve-containerization-docker and deploy on KServe.
    * Kserve can specify arguments to configure any deployment options. More information on Configuration option for inference service can be found [here](https://kserve.github.io/website/docs/model-serving/predictive-inference/frameworks/custom-predictor#arguments).
  * `aissemble-oip-kserve-containerization-docker`
    * This module contains docker file that can be built and run custom model for KServe.
    * Dockerfile is used to package inference code and model into docker image that kubernetes can deploy on KServe.
    * Docker containerization was leveraged using [Habushu containerize-dependencies goal](https://github.com/TechnologyBrewery/habushu/blob/dev/docs/HABUSHU_LIFECYCLE_README.md#containerize-dependencies) in which packages all necessary handler OIP files and dependencies into dockerfile.

## Configuration
This example demonstrates both methods of configuring the KServe server. While the example uses default values, it shows users exactly where and how to customize settings for their deployments.

### Properties File Configuration
The example includes an [oip.properties](../aissemble-oip-kserve-inference/src/resources/krausening/base/oip.properties) file that explicitly sets default values:
```properties
kserve_http_port=8080
```

### Environment Variable Configuration
The [inference-service.yaml](aissemble-oip-kserve-containerization-deploy/src/main/resources/templates/inference-service.yaml) shows how to override settings via environment variables:
```yaml
env:
  - name: KSERVE_HTTP_PORT
    value: "8080"
```

## Running REST Based Example
1. Run ```mvn clean install``` to make sure docker image can be generated to your docker daemon.
2. Create new namespace for testing purpose ```kubectl create namespace kserve-test```
3. cd into KServe deployment charts ```cd aissemble-open-inference-protocol-examples/aissemble-oip-kserve/aissemble-oip-kserve-containerization/aissemble-oip-kserve-containerization-deploy/src/main/resources/templates```
4. Apply Inference service helm chart to kserve-test namespace
   ```kubectl apply -n kserve-test -f ./inference-service.yaml```
5. Once predictor pod is ready, make sure kserve-model-predictor is port forwarding into 8080
6. Run curl command to send inference request.
``` 
curl --request POST \
   -H "Content-Type: application/json" \
   --url http://localhost:8080/v2/models/convert_celsius_to_fahrenheit/infer \
   --data '{
  "id": "1",
  "inputs": [
    {
      "name": "sample",
      "shape": [1,1],
      "datatype": "FP32",
      "data": [0.1]
    }
  ]
 }'
```

## Running gRPC Based Example
1. Run ```mvn clean install``` to make sure docker image can be generated to your docker daemon.
2. Create new namespace for testing purpose ```kubectl create namespace kserve-test```
3. cd into KServe deployment charts ```cd aissemble-open-inference-protocol-examples/aissemble-oip-kserve/aissemble-oip-kserve-containerization/aissemble-oip-kserve-containerization-deploy/src/main/resources/templates```
4. Apply Inference service helm chart to kserve-test namespace
   ```kubectl apply -n kserve-test -f ./inference-service-grpc.yaml```
5. Once predictor pod is ready, make sure kserve-model-predictor is port forwarding into 8081
6. cd into KServe inference example
```cd aissemble-open-inference-protocol-examples/aissemble-oip-kserve/aissemble-oip-kserve-inference```
7. Send an inference request to the gRPC service using grpc_client.py
```poetry run python ../aissemble-oip-kserve-containerization/sample_grpc_client.py```