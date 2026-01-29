"""Step definitions for module discovery and registration tests."""

from behave import given, when, then

from aissemble_inference_core.client.registry import ModuleRegistry
from aissemble_inference_yolo import YOLORuntime, YOLOTranslator


@given("the aissemble-inference-yolo package is installed")
def step_package_installed(context):
    """Verify the package is importable (which means it's installed)."""
    import aissemble_inference_yolo

    context.package = aissemble_inference_yolo


@when("I query the ModuleRegistry for available modules")
def step_query_registry(context):
    """Query the module registry for available modules."""
    ModuleRegistry.reset()
    context.registry = ModuleRegistry.instance()
    context.available_modules = context.registry.list_available()


@then('the "{module_name}" runtime should be listed')
def step_runtime_listed(context, module_name):
    """Verify a runtime is listed in the registry."""
    assert module_name in context.available_modules["runtimes"], (
        f"Expected '{module_name}' in runtimes, got: {context.available_modules['runtimes']}"
    )


@then('the "{module_name}" translator should be listed')
def step_translator_listed(context, module_name):
    """Verify a translator is listed in the registry."""
    assert module_name in context.available_modules["translators"], (
        f"Expected '{module_name}' in translators, got: {context.available_modules['translators']}"
    )


@when('I retrieve the "{module_name}" runtime from the registry')
def step_retrieve_runtime(context, module_name):
    """Retrieve a runtime class from the registry."""
    ModuleRegistry.reset()
    context.registry = ModuleRegistry.instance()
    context.retrieved_class = context.registry.get_runtime(module_name)


@then("I should receive the YOLORuntime class")
def step_verify_yolo_runtime(context):
    """Verify the retrieved class is YOLORuntime."""
    assert context.retrieved_class is YOLORuntime, (
        f"Expected YOLORuntime, got: {context.retrieved_class}"
    )


@when('I retrieve the "{module_name}" translator from the registry')
def step_retrieve_translator(context, module_name):
    """Retrieve a translator class from the registry."""
    ModuleRegistry.reset()
    context.registry = ModuleRegistry.instance()
    context.retrieved_class = context.registry.get_translator(module_name)


@then("I should receive the YOLOTranslator class")
def step_verify_yolo_translator(context):
    """Verify the retrieved class is YOLOTranslator."""
    assert context.retrieved_class is YOLOTranslator, (
        f"Expected YOLOTranslator, got: {context.retrieved_class}"
    )
