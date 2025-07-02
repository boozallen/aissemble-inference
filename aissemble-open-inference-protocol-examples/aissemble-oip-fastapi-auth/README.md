# aiSSEMBLE Open Inference Protocol Authorization Example
This example demonstrates calling inference endpoints with authorization enabled. While full 
authentication is out of scope, we will simulate authentication by generating a jwt token
that the authorization will then use to PERMIT or DENY an inference endpoint call. 


## Run the example
1. Ensure you have the `docker compose` utility.  If you don't have `docker compose`, you 
can follow [this guide](https://docs.docker.com/compose/install/) to install it. You will 
also need Poetry, so ensure you have it installed by following [this poetry install guide](https://python-poetry.org/docs/#installation)
2. Start the Authzforce server and the FastAPI server by running the following:
```sh
# Run the Authzforce server and the OIP REST server
python ./src/aissemble-oip-fastapi-auth/launch_example.py
```
3. Create the **authorized** jwt token (saved as an environment variable) by running the following in a terminal
```sh
export OIP_JWT=$(curl -s -H 'Content-Type: application/json' \
      -d '{
  "username": "alloweduser",
  "password": "password"
  }' \
      -X POST \
      http://127.0.0.1:8000/v2/login | jq -r .jwt)
```
4. Run an inference request with the jwt token
```sh
curl -X "POST" -w "\nHTTP Code: %{http_code}\n" \
  "http://127.0.0.1:8000/v2/models/my_model/infer" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $OIP_JWT" \
  -H "Content-Type: application/json" \
  -d '{
  "id": "string",
  "parameters": {
    "content_type": "string"
  },
  "inputs": [
    {
      "name": "string",
      "shape": [
        0
      ],
      "datatype": "BOOL",
      "parameters": {
        "content_type": "string"
      },
      "data": [
        "string"
      ]
    }
  ]
}'
```
5. Ensure you were permitted to run the inference request (`HTTP Code: 200`)
6. Now create a jwt token that is **unauthorized** (also saved as an environment variable)
```sh
export OIP_JWT=$(curl -s -H 'Content-Type: application/json' \
      -d '{
  "username": "notalloweduser",
  "password": "password"
  }' \
      -X POST \
      http://127.0.0.1:8000/v2/login | jq -r .jwt)
```
7. Re-run the inference request with the unauthorized token
```sh
curl -X "POST" -w "\nHTTP Code: %{http_code}\n" \
  "http://127.0.0.1:8000/v2/models/my_model/infer" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $OIP_JWT" \
  -H "Content-Type: application/json" \
  -d '{
  "id": "string",
  "parameters": {
    "content_type": "string"
  },
  "inputs": [
    {
      "name": "string",
      "shape": [
        0
      ],
      "datatype": "BOOL",
      "parameters": {
        "content_type": "string"
      },
      "data": [
        "string"
      ]
    }
  ]
}'
```
8. This time you should get a response from the server, indicating you were denied access (`HTTP Code: 403`).
9. Once you are done with the example you can use `ctrl + c` to shut down the services.
