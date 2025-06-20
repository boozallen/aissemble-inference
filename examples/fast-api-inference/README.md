# aiSSEMBLE Open Inference Protocol FastAPI Example
This example demonstrates how to hook model into Open Interface Protocol and use FastAPI to implement inference endpoint.
The example model is trained model that converts Celsius into Fahrenheit. 
The input will read as Celsius and output print as Fahrenheit value.

## Setting up the Project
We need to build and install dependencies before we can stand up fastAPI server.
Following command shall build and install dependencies.
```sh
mvnd clean install
```

## Running Example FastAPI
Start the FastAPI server using following command.
NOTE: poetry run command will use its .venv created from poetry when starting fastapi server. 
```sh
poetry run fastapi dev ./src/fast-api-inference/main.py
```

### Run Inference Endpoint
Run following Curl Command to send inference request.

```sh
curl -H 'Content-Type: application/json' \
      -d '{"id" : "2214",
  "inputs" : [{
      "name" : "sample",
      "shape" : [1],
      "datatype"  : "FP32",
      "data" : [ [ 25], [ 12 ] ]
  }]}' \
      -X POST \
      http://127.0.0.1:8000/v2/models/convert_celsius_to_fahrenheit/infer

```

