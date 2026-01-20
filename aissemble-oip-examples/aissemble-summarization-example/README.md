# aiSSEMBLE Summarization Example

This example demonstrates how to use the `aissemble-oip-sumy` module for text summarization with MLServer and the OIP Client.

## What This Example Demonstrates

- Integration between aissemble-oip-core, aissemble-oip-sumy, and MLServer
- Using the InferenceClient fluent API for text summarization
- Configuring MLServer with multiple summarization models
- Switching between summarization algorithms (TextRank, LSA, LexRank)
- BDD testing patterns for OIP-based applications
- End-to-end inference pipeline from text input to summary output

## Project Structure

```
aissemble-summarization-example/
├── models/                      # MLServer model configurations
│   ├── settings.json            # Global MLServer settings
│   ├── sumy-textrank/           # TextRank model
│   │   └── model-settings.json
│   └── sumy-lsa/                # LSA model
│       └── model-settings.json
├── src/                         # Package source
├── tests/
│   ├── test_data/               # Sample articles for testing
│   └── features/                # BDD tests
└── README.md
```

## Prerequisites

- Python 3.11 or higher
- uv package manager (`pip install uv`)
- aissemble-oip-core and aissemble-oip-sumy modules

## Installation

From the example directory:

```bash
uv sync --group test
```

This installs all dependencies including MLServer and the sumy library.

## Running Tests

The example includes comprehensive BDD tests using Behave:

```bash
uv run behave
```

Tests will:
1. Start MLServer with configured summarization models
2. Run inference scenarios with sample articles
3. Verify summary quality and format
4. Test error handling
5. Shutdown MLServer

## Usage Example

```python
from aissemble_oip_core.client import InferenceClient
from aissemble_oip_core.client.oip_adapter import HttpOipAdapter

# Create adapter pointing to MLServer
adapter = HttpOipAdapter(
    base_url="http://127.0.0.1:8080",
    model_name="sumy-textrank"
)

# Create client
client = InferenceClient(adapter=adapter, endpoint="http://127.0.0.1:8080")

# Read article text
with open("article.txt", "r") as f:
    article_text = f.read()

# Run summarization
result = client.summarize().text(article_text).run()

# Access summary
print(f"Original length: {result.original_length}")
print(f"Summary length: {result.summary_length}")
print(f"Summary: {result.summary}")
```

## Manual MLServer Operation

For development, you can run MLServer manually:

```bash
# Start MLServer (from example directory)
uv run mlserver start models

# In another terminal, run Python client code
uv run python your_script.py
```

MLServer will load both models:
- `sumy-textrank` at http://127.0.0.1:8080/v2/models/sumy-textrank/infer
- `sumy-lsa` at http://127.0.0.1:8080/v2/models/sumy-lsa/infer

## Components

### SumyRuntime
The MLServer runtime provided by `aissemble-oip-sumy`. Supports:
- TextRank, LSA, and LexRank algorithms
- Configurable sentence count
- Multi-language support

Configuration via `model-settings.json`:
```json
{
    "name": "sumy-textrank",
    "implementation": "aissemble_oip_sumy.SumyRuntime",
    "parameters": {
        "algorithm": "textrank",
        "sentences_count": 3,
        "language": "english"
    }
}
```

### HttpOipAdapter
HTTP client from `aissemble-oip-core` that communicates with MLServer:
- Handles text encoding and OIP protocol formatting
- Manages HTTP connections and retries
- Converts responses to SummarizationResult objects

### SummarizationBuilder
Fluent API for configuring summarization requests:
```python
client.summarize()
    .text("Long article...")
    .run()
```

### Test Features
BDD scenarios covering:
- Basic summarization with different article lengths
- Algorithm comparison (TextRank vs LSA)
- Parameter configuration
- Error handling (empty text, invalid config)

## Configuration Options

Model parameters in `model-settings.json`:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| algorithm | string | "textrank" | Summarization algorithm (textrank, lsa, lexrank) |
| sentences_count | int | 3 | Number of sentences in summary |
| language | string | "english" | Language for tokenization |

## Notes

- Sample articles in `tests/test_data/` are used for testing
- Summary quality depends on article structure and algorithm choice
- TextRank generally works well for most content
- LSA may perform better on technical documents
- NLTK data (punkt_tab) downloads automatically on first run

## Troubleshooting

**MLServer fails to start:**
- Check that port 8080 is available
- Verify aissemble-oip-sumy is installed: `uv pip show aissemble-oip-sumy`
- Check MLServer logs for errors

**Empty summaries:**
- Article may be too short (< sentences_count)
- Try different algorithm or reduce sentences_count
- Check that input text is not empty

**Import errors:**
- Run `uv sync --group test` to install dependencies
- Ensure you're in the correct directory
- Check that parent modules (core, sumy) are built

## License

Apache 2.0 - See LICENSE.txt
