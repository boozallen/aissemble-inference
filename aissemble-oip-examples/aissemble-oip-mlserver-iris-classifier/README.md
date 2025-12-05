# MLServer Iris Classifier Example

A simple example demonstrating MLServer basics with an OIP-compliant inference endpoint.

## Overview

This example shows how to serve a scikit-learn Logistic Regression model using MLServer. The model classifies iris flowers into three species based on sepal and petal measurements.

## Features

- **Model**: Logistic Regression trained on the classic Iris dataset
- **Input**: 4 features (sepal length, sepal width, petal length, petal width)
- **Output**: Predicted species class (0=setosa, 1=versicolor, 2=virginica) and probabilities

## Installation

```bash
uv sync
```

## Running the Server

```bash
uv run run_server
```

The server will start on `http://localhost:8080` by default.

## Making Predictions

Send a POST request to the inference endpoint:

```bash
curl -X POST http://localhost:8080/v2/models/iris-classifier/infer \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [{
      "name": "input",
      "shape": [1, 4],
      "datatype": "FP64",
      "data": [5.1, 3.5, 1.4, 0.2]
    }]
  }'
```

## API Endpoints

- `GET /v2/health/live` - Liveness check
- `GET /v2/health/ready` - Readiness check
- `GET /v2/models/iris-classifier` - Model metadata
- `POST /v2/models/iris-classifier/infer` - Run inference

