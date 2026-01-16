"""Step definitions for sumy module integration tests."""

import asyncio
from unittest.mock import Mock

from behave import given, then, when
from mlserver.settings import ModelParameters, ModelSettings
from mlserver.types import InferenceRequest, RequestInput

from aissemble_oip_core.client import InferenceClient, ModuleRegistry
from aissemble_oip_core.client.oip_adapter import OipAdapter, OipResponse, TensorData

# Sample text fixtures
SHORT_TEXT = """
Machine learning is transforming technology. It enables computers to learn from data.
Deep learning is a subset of machine learning. Neural networks power many AI systems.
"""

MEDIUM_TEXT = """
Artificial intelligence has revolutionized how we interact with technology. Machine learning,
a subset of AI, enables computers to learn patterns from data without explicit programming.
Deep learning, using neural networks with multiple layers, has achieved remarkable results
in image recognition, natural language processing, and game playing. These technologies are
now embedded in everyday applications from smartphone assistants to recommendation systems.
The future of AI promises even more sophisticated capabilities as computational power increases
and algorithms improve. However, ethical considerations around bias, privacy, and job
displacement remain important challenges to address.
"""

LONG_TEXT = """
The field of artificial intelligence has undergone remarkable transformations since its inception
in the 1950s. Early pioneers dreamed of creating machines that could think and reason like humans.
Today, we are witnessing the realization of many of those dreams through advances in machine
learning and deep learning technologies.

Machine learning represents a paradigm shift in how we program computers. Instead of explicitly
coding every rule and decision, we allow algorithms to learn patterns from vast amounts of data.
This approach has proven extraordinarily effective across numerous domains, from medical diagnosis
to financial forecasting to autonomous vehicle navigation.

Deep learning, a specialized branch of machine learning, uses artificial neural networks inspired
by the structure of the human brain. These networks consist of layers of interconnected nodes that
process information in increasingly abstract ways. The depth of these networks—hence the term
"deep learning"—allows them to capture incredibly complex patterns and relationships in data.

Natural language processing has been one of the most visible beneficiaries of deep learning
advances. Modern language models can generate coherent text, translate between languages, answer
questions, and even engage in surprisingly natural conversations. These capabilities have
transformed how we interact with technology, making it more accessible and intuitive.

Computer vision, another major application area, has seen dramatic improvements. Deep learning
models can now identify objects in images with accuracy rivaling or exceeding human performance.
This technology powers everything from photo organization apps to medical imaging systems that
detect diseases to autonomous vehicles that navigate complex environments.

The impact on healthcare has been particularly profound. AI systems assist doctors in diagnosing
diseases, predicting patient outcomes, and discovering new drugs. Machine learning algorithms
analyze medical images, genetic data, and patient records to identify patterns that might escape
human observation. These tools augment rather than replace human expertise, enabling more accurate
and timely medical interventions.

However, the rapid advancement of AI technologies raises important ethical and societal questions.
Issues of algorithmic bias, where AI systems perpetuate or amplify existing societal biases, demand
careful attention. Privacy concerns emerge as these systems require vast amounts of personal data.
The potential displacement of jobs by automation necessitates thoughtful policy responses and
workforce retraining initiatives.

Despite these challenges, the trajectory of AI development points toward even more transformative
applications. Researchers are working on systems that can reason more abstractly, learn from
smaller amounts of data, and explain their decisions more transparently. The integration of AI
into scientific research itself is accelerating discoveries across disciplines from physics to
biology to climate science.

As we stand at this technological inflection point, it is crucial to develop AI responsibly,
ensuring that these powerful tools benefit humanity broadly while mitigating potential harms.
The future will likely be shaped significantly by how we navigate these challenges and opportunities
in the years ahead.
"""


@given("the sumy module is installed")
def step_given_sumy_module_installed(context):
    """Verify the sumy module is installed and available."""
    # The module should be importable
    from aissemble_oip_sumy import SumyRuntime, SumyTranslator

    context.sumy_runtime_class = SumyRuntime
    context.sumy_translator_class = SumyTranslator


@when("I check the module registry")
def step_when_check_module_registry(context):
    """Check the module registry for registered components."""
    registry = ModuleRegistry.instance()
    context.registry_info = registry.list_available()


@then('the "{name}" runtime should be registered')
def step_then_runtime_registered(context, name):
    """Verify a runtime is registered in the registry."""
    assert "runtimes" in context.registry_info
    assert name in context.registry_info["runtimes"]


@then('the runtime class should be "{class_name}"')
def step_then_runtime_class(context, class_name):
    """Verify the runtime class name."""
    assert context.sumy_runtime_class.__name__ == class_name


@then('the "{name}" translator should be registered')
def step_then_translator_registered(context, name):
    """Verify a translator is registered in the registry."""
    assert "translators" in context.registry_info
    assert name in context.registry_info["translators"]


@then('the translator class should be "{class_name}"')
def step_then_translator_class(context, class_name):
    """Verify the translator class name."""
    assert context.sumy_translator_class.__name__ == class_name


@when('I retrieve the "{name}" runtime from the registry')
def step_when_retrieve_runtime(context, name):
    """Retrieve a runtime class from the registry."""
    registry = ModuleRegistry.instance()
    context.retrieved_runtime = registry.get_runtime(name)


@then("the runtime class should be importable")
def step_then_runtime_importable(context):
    """Verify the retrieved runtime class is importable and usable."""
    assert context.retrieved_runtime is not None
    assert callable(context.retrieved_runtime)


@when('I retrieve the "{name}" translator from the registry')
def step_when_retrieve_translator(context, name):
    """Retrieve a translator class from the registry."""
    registry = ModuleRegistry.instance()
    context.retrieved_translator = registry.get_translator(name)


@then("the translator class should be importable")
def step_then_translator_importable(context):
    """Verify the retrieved translator class is importable and usable."""
    assert context.retrieved_translator is not None
    assert callable(context.retrieved_translator)


@given('a model settings file with algorithm "{algorithm}"')
def step_given_model_settings_algorithm(context, algorithm):
    """Create model settings with specified algorithm."""
    parameters = ModelParameters(
        extra={"algorithm": algorithm, "sentences_count": 3, "language": "english"}
    )
    context.settings = ModelSettings(
        name="sumy-test",
        implementation="aissemble_oip_sumy.SumyRuntime",
        parameters=parameters,
    )


@given(
    'a model settings file with algorithm "{algorithm}" and sentences_count {count:d}'
)
def step_given_model_settings_with_count(context, algorithm, count):
    """Create model settings with algorithm and sentence count."""
    parameters = ModelParameters(
        extra={"algorithm": algorithm, "sentences_count": count, "language": "english"}
    )
    context.settings = ModelSettings(
        name="sumy-test",
        implementation="aissemble_oip_sumy.SumyRuntime",
        parameters=parameters,
    )


@given("I load the sumy runtime")
@when("I load the sumy runtime")
def step_when_load_runtime(context):
    """Load the sumy runtime with current settings."""
    from aissemble_oip_sumy import SumyRuntime

    context.runtime = SumyRuntime(context.settings)
    try:
        context.load_success = asyncio.run(context.runtime.load())
        context.load_error = None
    except Exception as e:
        context.load_success = False
        context.load_error = e


@then("the runtime should be ready")
def step_then_runtime_ready(context):
    """Verify the runtime is ready for inference."""
    assert context.load_success is True
    assert context.runtime.ready is True


@then('the algorithm should be "{algorithm}"')
def step_then_algorithm_is(context, algorithm):
    """Verify the configured algorithm."""
    assert context.runtime._algorithm == algorithm


@given("a short article text")
def step_given_short_text(context):
    """Provide a short article for testing."""
    context.input_text = SHORT_TEXT.strip()


@given("a medium article text")
def step_given_medium_text(context):
    """Provide a medium article for testing."""
    context.input_text = MEDIUM_TEXT.strip()


@given("a long article text with 10 paragraphs")
def step_given_long_text(context):
    """Provide a long article for testing."""
    context.input_text = LONG_TEXT.strip()


@when("I run inference on the text")
def step_when_run_inference(context):
    """Run inference on the input text."""
    payload = InferenceRequest(
        inputs=[
            RequestInput(
                name="text", shape=[1], datatype="BYTES", data=[context.input_text]
            )
        ]
    )
    try:
        context.response = asyncio.run(context.runtime.predict(payload))
        context.inference_error = None
    except Exception as e:
        context.response = None
        context.inference_error = e


@then("I should receive a summary")
def step_then_receive_summary(context):
    """Verify a summary is returned."""
    assert context.response is not None
    assert len(context.response.outputs) > 0
    summary_output = context.response.outputs[0]
    assert summary_output.name == "summary"
    assert len(summary_output.data) > 0
    context.summary = summary_output.data[0]


@then("the summary should be shorter than the original text")
def step_then_summary_shorter(context):
    """Verify the summary is shorter than the input."""
    assert len(context.summary) < len(context.input_text)


@then("the summary should not be empty")
def step_then_summary_not_empty(context):
    """Verify the summary is not empty."""
    assert context.summary is not None
    assert len(context.summary.strip()) > 0


@then("the summary should contain approximately {count:d} sentences")
def step_then_summary_sentence_count(context, count):
    """Verify the summary has approximately the expected sentence count."""
    # Count sentences (rough approximation)
    sentence_count = (
        context.summary.count(".")
        + context.summary.count("!")
        + context.summary.count("?")
    )
    # Allow for some variance (±1 sentence)
    assert abs(sentence_count - count) <= 1


@given("an empty text input")
def step_given_empty_text(context):
    """Provide an empty text input."""
    context.input_text = "   "


@then("inference should raise a ValueError")
def step_then_inference_raises_value_error(context):
    """Verify that inference raised a ValueError."""
    assert context.inference_error is not None
    assert isinstance(context.inference_error, ValueError)


@then('the error message should mention "{text}"')
def step_then_error_message_contains(context, text):
    """Verify the error message contains expected text."""
    # Check both inference_error and load_error
    error = getattr(context, "inference_error", None) or getattr(
        context, "load_error", None
    )
    assert error is not None, "No error found in context"
    error_msg = str(error).lower()
    assert text.lower() in error_msg


@then("loading should raise a ValueError")
def step_then_loading_raises_value_error(context):
    """Verify that loading raised a ValueError."""
    assert context.load_error is not None
    assert isinstance(context.load_error, ValueError)


@given("an empty payload with no inputs")
def step_given_empty_payload(context):
    """Create an empty payload for testing error handling."""
    context.empty_payload = InferenceRequest(inputs=[])


@when("I run inference on the payload")
def step_when_run_inference_on_payload(context):
    """Run inference on a pre-created payload."""
    try:
        context.response = asyncio.run(context.runtime.predict(context.empty_payload))
        context.inference_error = None
    except Exception as e:
        context.response = None
        context.inference_error = e


@given("a mock OIP adapter")
def step_given_mock_adapter(context):
    """Create a mock OIP adapter for testing."""
    context.mock_adapter = Mock(spec=OipAdapter)


@given("the adapter returns a valid summary response")
def step_given_adapter_returns_summary(context):
    """Configure the mock adapter to return a summary response."""
    mock_response = OipResponse(
        model_name="sumy",
        outputs=[
            TensorData(
                name="summary",
                shape=[1],
                datatype="BYTES",
                data=[["This is a test summary of the input text."]],
            )
        ],
    )
    context.mock_adapter.infer.return_value = mock_response


@when("I use InferenceClient to summarize text")
def step_when_use_inference_client(context):
    """Use the InferenceClient to summarize text."""
    client = InferenceClient(adapter=context.mock_adapter, endpoint="http://test:8080")
    context.client_result = (
        client.summarize("sumy").text("This is a long article to summarize.").run()
    )


@then("I should receive a SummarizationResult")
def step_then_receive_summarization_result(context):
    """Verify a SummarizationResult is returned."""
    assert context.client_result is not None
    assert hasattr(context.client_result, "summary")


@then("the result should contain the summary text")
def step_then_result_contains_summary(context):
    """Verify the result contains summary text."""
    assert context.client_result.summary is not None
    assert len(context.client_result.summary) > 0
