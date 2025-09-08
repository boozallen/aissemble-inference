import nose.tools as nt
from behave import given, then, when


from handlers.test_kserve_handler import KserveCustomHandler


@given("KServe custom handler with ability to load keras model")
def given_kserve_handler(context):
    context.handler = KserveCustomHandler(name="test", model_path="test_model")


@when("Load API executed using the KServe custom handler")
def when_i_send_convert_inference_request(context):
    context.result = context.handler.model_load()


@then("load is successful and model server status is set to ready")
def inference_request_correctly_returned(context):
    nt.assert_true(context.handler.ready, "model should be ready")
    nt.assert_is_not_none(context.handler.model, "model should not be None")
