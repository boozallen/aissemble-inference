"""Step definitions for summarization tests."""

import os

from behave import given, then, when

from aissemble_oip_core.client import InferenceClient
from aissemble_oip_core.client.oip_adapter import HttpOipAdapter


@given("MLServer is running with the Sumy model")
def step_mlserver_running(context):
    """Verify MLServer is available."""
    assert hasattr(context, "mlserver_url")
    assert hasattr(context, "test_data_dir")


@given("I have a {size} article text")
def step_have_article(context, size):
    """Load article text from test data."""
    filename = f"{size}_article.txt"
    filepath = os.path.join(context.test_data_dir, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        context.article_text = f.read()

    assert len(context.article_text) > 0


@given("I have empty text")
def step_have_empty_text(context):
    """Set empty text for error testing."""
    context.article_text = ""


@when("I run summarization using the OIP client")
def step_run_summarization(context):
    """Execute summarization with default model."""
    adapter = HttpOipAdapter(base_url=context.mlserver_url, model_name="sumy-textrank")
    client = InferenceClient(adapter=adapter, endpoint=context.mlserver_url)

    try:
        context.result = client.summarize().text(context.article_text).run()
        context.error = None
    except Exception as e:
        context.result = None
        context.error = e


@when('I run summarization using the OIP client with model "{model_name}"')
def step_run_summarization_with_model(context, model_name):
    """Execute summarization with specific model."""
    adapter = HttpOipAdapter(base_url=context.mlserver_url, model_name=model_name)
    client = InferenceClient(adapter=adapter, endpoint=context.mlserver_url)

    context.result = client.summarize().text(context.article_text).run()
    context.error = None


@when("I attempt to run summarization")
def step_attempt_summarization(context):
    """Try to summarize (for error testing)."""
    adapter = HttpOipAdapter(base_url=context.mlserver_url, model_name="sumy-textrank")
    client = InferenceClient(adapter=adapter, endpoint=context.mlserver_url)

    try:
        context.result = client.summarize().text(context.article_text).run()
        context.error = None
    except Exception as e:
        context.result = None
        context.error = e


@then("I should receive a summary")
def step_receive_summary(context):
    """Verify summary result is present."""
    assert context.result is not None
    assert hasattr(context.result, "summary")
    assert context.result.summary is not None
    context.summary = context.result.summary


@then("I should receive an error response")
def step_receive_error(context):
    """Verify error was raised."""
    assert context.error is not None or (
        context.result is not None and hasattr(context.result, "error")
    )


@then("the summary should be shorter than the original text")
def step_summary_shorter(context):
    """Verify compression occurred."""
    assert len(context.summary) < len(context.article_text)


@then("the summary should not be empty")
def step_summary_not_empty(context):
    """Verify summary contains content."""
    assert len(context.summary.strip()) > 0


@then("the summary should contain approximately {count:d} sentences")
def step_summary_sentence_count(context, count):
    """Verify sentence count (rough approximation)."""
    sentence_count = (
        context.summary.count(".")
        + context.summary.count("!")
        + context.summary.count("?")
    )
    assert abs(sentence_count - count) <= 2, (
        f"Expected approximately {count} sentences, "
        f"but got {sentence_count}. Summary: {context.summary}"
    )


@then("the summary should be significantly shorter than the original")
def step_summary_significantly_shorter(context):
    """Verify substantial compression."""
    compression_ratio = len(context.summary) / len(context.article_text)
    assert compression_ratio < 0.3, (
        f"Expected at least 70% reduction, "
        f"but got {compression_ratio:.2%}. "
        f"Original: {len(context.article_text)} chars, "
        f"Summary: {len(context.summary)} chars"
    )


@then("the summary should contain key information from the article")
def step_summary_contains_key_info(context):
    """Verify summary relevance (basic check)."""
    original_words = set(context.article_text.lower().split())
    summary_words = set(context.summary.lower().split())

    overlap = len(summary_words & original_words) / len(summary_words)
    assert overlap > 0.4, (
        f"Expected at least 40% word overlap, but got {overlap:.2%}. "
        f"This may indicate the summary is not relevant to the original text."
    )


@then("the summary should be grammatically coherent")
def step_summary_coherent(context):
    """Basic coherence check."""
    assert context.summary[0].isupper(), "Summary should start with capital letter"

    assert context.summary[-1] in ".!?", "Summary should end with proper punctuation"

    assert any(punct in context.summary for punct in ".!?"), (
        "Summary should contain at least one complete sentence"
    )
