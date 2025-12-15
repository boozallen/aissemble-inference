"""
Client script to test the MLServer object detection inference endpoint.

Usage:
    uv run python client.py <path_to_image>

Example:
    uv run python client.py /path/to/image.jpg
"""

import base64
import json
import sys
from pathlib import Path
import requests


def encode_image(image_path: str) -> str:
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as f:
        image_bytes = f.read()
        return base64.b64encode(image_bytes).decode("utf-8")


def run_inference(image_path: str, server_url: str = "http://localhost:8080") -> dict:
    """
    Send an image to the object detection model and get predictions.
    
    Args:
        image_path: Path to the image file
        server_url: Base URL of the MLServer instance
        
    Returns:
        Dictionary containing the inference response
    """
    # encode image
    image_b64 = encode_image(image_path)
    
    # create payload that matches expected input
    payload = {
        "inputs": [
            {
                "name": "image",
                "shape": [1],
                "datatype": "BYTES",
                "data": [image_b64]
            }
        ]
    }
    
    # create endpoint url address to hit our predict endpoint
    inference_url = f"{server_url}/v2/models/img-detection/infer"
    response = requests.post(inference_url, json=payload) # pass payload
    response.raise_for_status() # check for any exceptions in our request and raise them
    
    return response.json()


def format_results(response: dict) -> None:
    """Pretty print the inference results."""
    print("\n" + "="*60)
    print("Object Detection Results")
    print("="*60)
    
    # gather outputs - data field from type REsponseObject
    outputs = {output["name"]: output["data"] for output in response["outputs"]}
    
    labels = outputs.get("labels", [])
    scores = outputs.get("scores", [])
    boxes_flat = outputs.get("boxes", [])
    
    # reshape boxes from flat list to list of [xmin, ymin, xmax, ymax]
    boxes = [boxes_flat[i:i+4] for i in range(0, len(boxes_flat), 4)]
    
    if not labels:
        print("No objects detected.")
        return
    
    print(f"\nDetected {len(labels)} object(s):\n")
    
    for i, (label, score, box) in enumerate(zip(labels, scores, boxes), 1):
        xmin, ymin, xmax, ymax = box
        print(f"{i}. {label}")
        print(f"   Confidence: {score:.2%}")
        print(f"   Bounding Box: [{xmin:.1f}, {ymin:.1f}, {xmax:.1f}, {ymax:.1f}]")
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python client.py <path_to_image>")
        print("Example: uv run python client.py /path/to/image.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not Path(image_path).exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    
    print(f"Sending image to inference endpoint: {image_path}")
    
    try:
        response = run_inference(image_path)
        format_results(response)
        
        # save full response to JSON
        print("="*60)
        print("Full response saved to: inference_response.json")
        with open("inference_response.json", "w") as f:
            json.dump(response, f, indent=2)
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server.")
        print("Make sure the server is running with:")
        print("  uv run python src/object_detection/server.py")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()