# aiSSEMBLE Open Inference Protocol FastAPI Example
This example demonstrates how to hook model into Open Interface Protocol and use FastAPI to implement inference endpoint.
The example model is trained model that converts Celsius into Fahrenheit. 
The input will read as Celsius and output print as Fahrenheit value.

## Running the example

1. Build and install dependencies to prepare the fastAPI server by running the following Poetry command.
```sh
poetry install
```
2. Start the FastAPI server using the following command.
```sh
# NOTE: This poetry run command will start the FastAPI server using the local .venv.
poetry run fastapi dev ./src/aissemble-oip-fastapi-inference/main.py
```
3. Run the following curl commands to send the corresponding request.

| API              | Command                                                                                                                                                                                                                                                                                                                                             |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Inference        | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-d '{"id" : "2214",<br/>"inputs" : [{<br/>"name" : "sample",<br/>"shape" : [1],<br/>"datatype"  : "FP32",<br/>"data" : [ [ 25], [ 12 ] ]<br/>}]}' \\<br/>-X POST \\<br/>http://127.0.0.1:8000/v2/models/convert_celsius_to_fahrenheit/infer </pre> |
| Model Metadata   | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-X GET \\<br/>http://127.0.0.1:8000/v2/models/convert_celsius_to_fahrenheit</pre>|
| Server Ready     | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-X GET \\<br/>http://127.0.0.1:8000/v2/health/ready</pre>|
| Server Live     | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-X GET \\<br/>http://127.0.0.1:8000/v2/health/live</pre>|
| Server Metadata     | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-X GET \\<br/>http://127.0.0.1:8000/v2</pre>|
| Model Ready     | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-X GET \\<br/>http://127.0.0.1:8000/v2/models/convert_celsius_to_fahrenheit/ready</pre>|

