# OIP Core Tests

BDD tests for the aiSSEMBLE Inference Core library using Behave.

## Running Tests

From the `aissemble-inference-core` directory:

```bash
# Install test dependencies
uv sync --group test

# Run all tests
behave

# Run specific feature
behave tests/features/invoke-object-detection.feature

# Run with verbose output
behave -v
```

## Directory Structure

```
tests/
├── features/              # Feature files and step definitions
│   ├── steps/            # Step implementations
│   ├── environment.py    # Test hooks
│   └── *.feature         # BDD scenarios
└── test_data/            # Test fixtures
```
