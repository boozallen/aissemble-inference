# aiSSEMBLE Open Inference Protocol KServe Example
This example demonstrates how to hook model into Open Interface Protocol and use KServe to implement inference endpoint.


## Prerequisites
* Helm
* kubectl
* docker

## Install KServe Infrastructure app

Below are all the necessary infrastructures to run the Kserve app. These deployments just need to be
run once in the env. It contains 4 services: Cert-Manager, NGINX, Kserve CRDs, and the Kserve controller.

## Building Helm charts
Run the following to install the helm dependent charts:
```bash
helm dependency build ./cert-manager/
helm dependency build ./kserve-crds/
helm dependency build ./kserve/
helm dependency build ./nginx/
```

## Services

### CustomResourceDefinition
Kserve requires several custom resources to run. To install:
```bash
helm install kserve-crds ./kserve-crds/
```

### Ingress NGINX
Google Cloud has their own ingress GCE. For this project, we will use NGINX. To install:
```bash
helm install ingress-nginx ./nginx/ --namespace ingress-nginx --create-namespace
```

### Cert-Manager
Cert manager is required to provision webhook certs for production grade installation. To install:
```bash
helm install cert-manager ./cert-manager/ --create-namespace --namespace cert-manager
```

### Kserve Controller
The Kserve controller is the brains behind standing up the Kserve application. This project is using the Raw
Deployment mode. To install:
```bash
helm install kserve ./kserve/
```

### Tear Down
Note these are infrastructure services so any application using them on the cluster will fail if taken down!
To tear down the infrastructure run:
```bash
helm uninstall kserve
helm uninstall kserve-crds
helm uninstall cert-manager --namespace cert-manager
helm uninstall ingress-nginx --namespace ingress-nginx
```


## Running KServe Example app

Build Docker Images
In order to run Kserve, we need to build kserve model images first using following command
```bash
docker build -t kserve-model:0.1.1 {your-path-to-repo}/aissemble-open-inference-protocol-examples/aissemble-oip-kserve/aissemble-oip-kserve-inference/
```

Create a test namespace
```bash
kubectl create namespace kserve-test
```

Apply Inference service helm chart to kserve-test namespace
```bash
kubectl apply -n kserve-test -f ./inference-service.yaml
```
check status of pods until predictor pod is ready
```bash
kubectl get pods -n kserve-test
```

Run Curl Command to send inference Request

``` bash
curl --request POST \
-H "Content-Type: application/json" \
--url http://localhost:8080/v2/models/kserve-model/infer \
--data '{
"id" : "1",
"inputs" : [
{
"name" : "sample",
"shape" : [1],
"datatype"  : "FP32",
"parameters": {
"content_type": "str"
},
"data" : [[ 0]]
}
]
}'
```

You will get Response something like this:

```bash
{"model_name":"kserve-model","model_version":null,"id":"1","parameters":null,"outputs":[{"name":"kserve-model","shape":[1],"datatype":"FP32","parameters":null,"data":[31.86412239074707]}]}%                      
```


### Tear down
To tear down the application, delete the namespace
```bash
kubectl delete namespace kserve-test
```