from aissemble_oip.client.inference_client import InferenceClient #type: ignore
from aissemble_oip.client.oip_adapter import OipAdapter #type: ignore

print("Imports successful!")

# initialize object
adapter = OipAdapter()
client = InferenceClient(adapter=adapter, endpoint="http:''localhost:8000")

# pass in data and print out
print('Client created!')
print(f"    endpoint: {client.endpoint}")
print(f"    adapter: {client.adapter}")