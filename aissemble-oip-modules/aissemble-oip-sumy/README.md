# aiSSEMBLE OIP Sumy Module

Sumy library integration for text summarization support in the aiSSEMBLE Open Inference Protocol library.

## Supported Algorithms

This module supports multiple summarization algorithms through the sumy library:

| Algorithm | Description |
|-----------|-------------|
| TextRank | Graph-based ranking algorithm (default) |
| LSA | Latent Semantic Analysis |
| LexRank | Graph-based ranking with cosine similarity |

## Installation

```bash
pip install aissemble-oip-sumy
```

This will also install the required dependencies:
- `aissemble-oip-core`
- `sumy` (text summarization library)
- `nltk` (natural language processing toolkit)

## Usage

### With MLServer

Create a `model-settings.json`:

```json
{
    "name": "sumy",
    "implementation": "aissemble_oip_sumy.SumyRuntime",
    "parameters": {
        "algorithm": "textrank",
        "sentences_count": 3,
        "language": "english"
    }
}
```

Start MLServer:

```bash
mlserver start /path/to/models
```

### With OIP Client

```python
from aissemble_oip_core.client import InferenceClient
from aissemble_oip_core.client.registry import ModuleRegistry

# The module auto-registers via entry points
print(ModuleRegistry.instance().list_available())
# {'runtimes': ['sumy', ...], 'translators': ['sumy', ...], ...}

# Use with InferenceClient
client = InferenceClient(adapter, endpoint)
result = client.summarize("sumy").text("Long article text...").run()
print(result.summary)
```

## Components

### SumyRuntime

MLServer-compatible runtime that wraps sumy summarization algorithms:
- Accepts text strings via OIP protocol
- Returns summarized text
- Configurable algorithm, sentence count, and language via parameters

### SumyTranslator

Translator for sumy outputs:
- Inherits from `DefaultSummarizationTranslator`
- Can be extended with sumy-specific optimizations

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `algorithm` | string | "textrank" | Summarization algorithm (textrank, lsa, lexrank) |
| `sentences_count` | int | 3 | Number of sentences in the summary |
| `language` | string | "english" | Language for text tokenization |

**Note**: The `max_length` and `min_length` parameters from `SummarizationBuilder` are not currently supported by this module. This is planned for a future enhancement.

## Entry Points

This module registers the following entry points:

| Group | Name | Class |
|-------|------|-------|
| `oip.runtimes` | sumy | `SumyRuntime` |
| `oip.translators` | sumy | `SumyTranslator` |

## Language Support

The sumy library supports multiple languages for tokenization and stemming. Specify the language using the `language` parameter in `model-settings.json`. Common languages include:

- english
- spanish
- french
- german
- italian
- portuguese
- russian
- czech
- slovak

Refer to the [sumy documentation](https://github.com/miso-belica/sumy) for a complete list of supported languages.

## Testing

This module includes comprehensive tests covering:

### Unit Tests
- Module registration and discovery
- Runtime loading with different algorithms
- Direct inference via SumyRuntime
- Translator functionality
- Error handling and validation

### Integration Tests (tagged with `@integration`)
- End-to-end OIP communication via MLServer
- Real HTTP requests using InferenceClient
- Algorithm switching (TextRank, LSA, LexRank)
- Parameter configuration validation

Run tests:

```bash
# Run all tests (unit + integration)
mvn clean install

# Run only unit tests (excluding @integration tag)
behave --tags=-integration
```

The integration tests automatically:
1. Start MLServer with configured models
2. Execute real inference requests via OIP protocol
3. Validate responses and summaries
4. Clean up resources

See `tests/features/` for test scenarios and `tests/features/environment.py` for MLServer test infrastructure.

## Example

For a complete working example, see the `aissemble-summarization-example` in the examples directory:

```bash
cd aissemble-oip-examples/aissemble-summarization-example
uv sync --group test
uv run behave
```

The example demonstrates:
- MLServer configuration for multiple summarization algorithms
- Integration with InferenceClient and HttpOipAdapter
- BDD test patterns for OIP-based applications
- Sample article data for testing
