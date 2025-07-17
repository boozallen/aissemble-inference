# aiSSEMBLE Open Inference Protocol Shared Utils
Contains common functionality shared across multiple interfaces

### Getting Started
Add the `aissemble-open-inference-protocol-shared` module as  Poetry dependency

```
poetry add -e ../aissemble-open-inference-protocol-shared
```
The following dependency specification will be added to the pipeline's `pyproject.toml` configuration:

```
[tool.poetry.dependencies]
aissemble-open-inference-protocol-shared = {path = "../aissemble-open-inference-protocol-shared", develop = true}
```

## Features

### content_type Parameter (Work In Progress)
The `content_type` feature lets you declare, at either request time or in model metadata, how each OIP-compliant input should be converted into a Python object.

**Declaring Content Types**

Content types are listed in order of precedence.
- **Input Level**: Include a `content_type` field under each `inputs[].parameters` in the request JSON. This will apply the content type to the particular input only.
- **Request Level**: Include a `content_type` field at the top-level `parameters` tag of the request JSON. This will decode the entire request into one a single Python object.


**Example:**
```json
{
  "model_name": "my_model",
  "id": "id-123",
  "parameters": {
    "content_type": "str"
  },
  "inputs": [
    {
      "name": "input-0",
      "datatype": "BYTES",
      "shape": [2,1],
      "parameters": {
        "content_type": "str"
      },
      "data": ["Hello","World"]
    }
  ]
}
```

**Creating Your Own Custom Codec:**
   1. **Input‐level codec**
       - Subclass `aissemble_open_inference_protocol_shared.codecs.codec.InputCodec`
       - Set `ContentType = "<your-type>"`
       - Implement:
           - `can_encode(payload) -> bool`
           - `encode_input(name, payload) -> RequestInput`
           - `decode_input(RequestInput) -> payload`
           - `encode_output(name, payload) -> ResponseOutput`
           - `decode_output(ResponseOutput) -> payload`
       - Decorate your class with `@register_input_codec`

   2. **Request‐level codec**
       - Subclass `aissemble_open_inference_protocol_shared.codecs.codec.SingleTensorRequestCodec` (or `aissemble_open_inference_protocol_shared.codecs.codec.RequestCodec`)
       - Set:
           - `ContentType = "<your-type>"`
           - `InputCodec   = YourInputCodecClass`
       - Optionally override `encode_request`/`decode_request` or `encode_response`/`decode_response`
       - Decorate with `@register_request_codec`

Once registered, any request or response tagged with `"content_type":"<your-type>"` will use your codec automatically.  