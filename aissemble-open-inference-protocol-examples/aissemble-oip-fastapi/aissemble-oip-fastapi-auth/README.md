[[Return to Examples Documentation]](../../README.md)

# aiSSEMBLE&trade; Open Inference Protocol FastAPI Authorization Example
This example demonstrates calling inference endpoints with authorization enabled. While full 
authentication is out of scope, we will simulate authentication by generating a jwt token
that the authorization will then use to PERMIT or DENY an inference endpoint call. 

This example uses an Authzforce adapter we have created. This gives a good jumping off point but if you want to 
create your own custom auth implementation, you can override the abstract class [auth adapter base](https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-shared/src/aissemble_open_inference_protocol_shared/auth/auth_adapter_base.py) and pass it to the AissembleOIPFastAPI server.

## Getting Started
- Ensure you have the `docker compose` utility installed.  If not, follow the [Docker Compose installation guide](https://docs.docker.com/compose/install/)
- Ensure you have Poetry installed. If not, follow the [Poetry installation guide](https://python-poetry.org/docs/#installation)
- Build and install all dependencies to prepare the FastAPI server by running the following Poetry command:
    ```bash
    poetry install
    ```

## Running the Example
1. Start the Authzforce server and the FastAPI server by running the following:
    ```sh
    python ./src/aissemble_oip_fastapi_auth/launch_example.py
    ```
2. Create the **authorized** jwt token (saved as an environment variable) by running the following in a terminal
    ```sh
    export OIP_JWT=$(curl -s -H 'Content-Type: application/json' \
          -d '{
      "username": "alloweduser",
      "password": "password"
      }' \
          -X POST \
          http://127.0.0.1:8000/v2/login | jq -r .jwt)
    ```
3. Run an inference request with the jwt token
    ```sh
    curl -X "POST" -w "\nHTTP Code: %{http_code}\n" \
      "http://127.0.0.1:8000/v2/models/my_model/infer" \
      -H "accept: application/json" \
      -H "Authorization: Bearer $OIP_JWT" \
      -H "Content-Type: application/json" \
      -d '{
      "id": "string",
      "parameters": {
        "content_type": "str"
      },
      "inputs": [
        {
          "name": "string",
          "shape": [
            1
          ],
          "datatype": "BYTES",
          "parameters": {
            "content_type": "str"
          },
          "data": [
            "string"
          ]
        }
      ]
    }'
    ```
4. Ensure you were permitted to run the inference request (`HTTP Code: 200`)
5. Now create a jwt token that is **unauthorized** (also saved as an environment variable)
    ```sh
    export OIP_JWT=$(curl -s -H 'Content-Type: application/json' \
          -d '{
      "username": "notalloweduser",
      "password": "password"
      }' \
          -X POST \
          http://127.0.0.1:8000/v2/login | jq -r .jwt)
    ```
6. Re-run the inference request with the unauthorized token
    ```sh
    curl -X "POST" -w "\nHTTP Code: %{http_code}\n" \
      "http://127.0.0.1:8000/v2/models/my_model/infer" \
      -H "accept: application/json" \
      -H "Authorization: Bearer $OIP_JWT" \
      -H "Content-Type: application/json" \
      -d '{
      "id": "string",
      "parameters": {
        "content_type": "str"
      },
      "inputs": [
        {
          "name": "string",
          "shape": [
            1
          ],
          "datatype": "BYTES",
          "parameters": {
            "content_type": "str"
          },
          "data": [
            "string"
          ]
        }
      ]
    }'
    ```
7. This time you should get a response from the server, indicating you were denied access (`HTTP Code: 403`).
8. Once you are done with the example you can use `ctrl + c`/`cmd + c` to shut down the services.
