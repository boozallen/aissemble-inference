[[Return to Examples Documentation]](../../README.md)

# aiSSEMBLE Open Inference Protocol&trade; FastAPI Inference Example
This example demonstrates how to integrate a model with the Open Interface Protocol using FastAPI to implement an inference endpoint.
The example model takes Celsius as input and returns the corresponding Fahrenheit value as output.

## Getting Started
- Ensure you have Poetry installed. If not, follow the [Poetry installation guide](https://python-poetry.org/docs/#installation)
- Build and install all dependencies to prepare the FastAPI server by running the following Poetry command:
    ```bash
    poetry install
    ```

## Running the Example

1. Start the FastAPI server using the following command.
    ```sh
    # NOTE: This poetry run command will start the FastAPI server using the local .venv.
    poetry run fastapi dev ./src/aissemble_oip_fastapi_inference/main.py
    ```
   
2. Run the following curl commands to send the corresponding request.
   
   | API             | Command                                                                                                                                                                                                                                                                                                                                      |
   |-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
   | Inference       | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-d '{"id" : "2214",<br/>"inputs" : [{<br/>"name" : "sample",<br/>"shape" : [2,1],<br/>"datatype"  : "INT32",<br/>"data" : [[25],[12]]<br/>}]}' \\<br/>-X POST \\<br/>http://127.0.0.1:8000/v2/models/convert_celsius_to_fahrenheit/infer </pre> |
   | Model Metadata  | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-X GET \\<br/>http://127.0.0.1:8000/v2/models/convert_celsius_to_fahrenheit</pre>                                                                                                                                                               |
   | Server Ready    | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-X GET \\<br/>http://127.0.0.1:8000/v2/health/ready</pre>                                                                                                                                                                                       |
   | Server Live     | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-X GET \\<br/>http://127.0.0.1:8000/v2/health/live</pre>                                                                                                                                                                                        |
   | Server Metadata | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-X GET \\<br/>http://127.0.0.1:8000/v2</pre>                                                                                                                                                                                                    |
   | Model Ready     | <pre>curl -w "\nHTTP Code: %{http_code}\n" \\<br/>-H 'Content-Type: application/json' \\<br/>-X GET \\<br/>http://127.0.0.1:8000/v2/models/convert_celsius_to_fahrenheit/ready</pre>                                                                                                                                                         |

