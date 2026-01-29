"""Step definitions for InferenceClient OIP integration tests."""

import sys
from pathlib import Path

from behave import given, then, when

from aissemble_inference_core.client import InferenceClient
from aissemble_inference_core.client.oip_adapter import HttpOipAdapter
from aissemble_inference_core.client.results import SummarizationResult


def _get_start_mlserver_func():
    """Lazily import start_mlserver_with_model from environment.py."""
    features_dir = Path(__file__).parent.parent
    if str(features_dir) not in sys.path:
        sys.path.insert(0, str(features_dir))
    from environment import start_mlserver_with_model

    return start_mlserver_with_model


@given('MLServer is running with Sumy model using "{algorithm}" algorithm')
def step_mlserver_running_with_algorithm(context, algorithm):
    """Start MLServer with specified algorithm."""
    start_mlserver = _get_start_mlserver_func()
    start_mlserver(context, algorithm=algorithm, sentences_count=3)


@given(
    'MLServer is running with Sumy model using "{algorithm}" algorithm with {count:d} sentences'
)
def step_mlserver_running_with_algorithm_and_count(context, algorithm, count):
    """Start MLServer with specified algorithm and sentence count."""
    start_mlserver = _get_start_mlserver_func()
    start_mlserver(context, algorithm=algorithm, sentences_count=count)


@given("I have an InferenceClient configured with HttpOipAdapter")
def step_have_inference_client(context):
    """Create an InferenceClient with HTTP adapter."""
    adapter = HttpOipAdapter(context.mlserver_url, "sumy")
    context.client = InferenceClient(adapter, context.mlserver_url)
    context.adapter = adapter


@given("I load a sample article from test data")
def step_load_sample_article(context):
    """Load sample article text from test data."""
    test_data_dir = Path(__file__).parent.parent.parent / "test-data"
    article_path = test_data_dir / "sample_article.txt"

    if not article_path.exists():
        raise FileNotFoundError(f"Sample article not found at {article_path}")

    with open(article_path, "r", encoding="utf-8") as f:
        context.input_text = f.read()

    assert len(context.input_text) > 0, "Sample article is empty"


@when("I call summarize and provide the text")
def step_call_summarize(context):
    """Call summarize with the input text."""
    try:
        context.summarization_result = (
            context.client.summarize().text(context.input_text).run()
        )
        context.summarization_error = None
    except Exception as e:
        context.summarization_result = None
        context.summarization_error = e


@then("I should receive a SummarizationResult via OIP")
def step_receive_summarization_result_via_oip(context):
    """Verify a SummarizationResult was returned via OIP."""
    if context.summarization_error:
        raise AssertionError(f"Summarization failed: {context.summarization_error}")
    assert context.summarization_result is not None, "No result received"
    assert isinstance(context.summarization_result, SummarizationResult), (
        f"Expected SummarizationResult, got {type(context.summarization_result)}"
    )
    assert hasattr(context.summarization_result, "summary")
    assert context.summarization_result.summary is not None
    context.summary = context.summarization_result.summary


@then("the summary should contain approximately {count:d} sentences via OIP")
def step_summary_sentence_count_via_oip(context, count):
    """Verify the summary has approximately the expected sentence count."""
    sentence_count = (
        context.summary.count(".")
        + context.summary.count("!")
        + context.summary.count("?")
    )
    # Allow for some variance (±2 sentences since algorithms can vary)
    assert abs(sentence_count - count) <= 2, (
        f"Expected approximately {count} sentences, "
        f"but got {sentence_count}. Summary: {context.summary}"
    )
