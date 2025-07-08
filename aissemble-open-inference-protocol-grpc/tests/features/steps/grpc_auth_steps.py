import grpc
import jwt
import asyncio
from behave import given, when, then
import nose.tools as nt
from aissemble_open_inference_protocol_shared.config.oip_config import OIPConfig
from aissemble_open_inference_protocol_grpc.auth.auth_interceptor import AuthInterceptor
from aissemble_open_inference_protocol_shared.auth.default_adapter import DefaultAdapter
from steps.utils.auth_test_utils import AuthTestHelper, METHOD_NAME

SERVER_ADDRESS = "localhost:8080"
SECRET_KEY = OIPConfig().auth_secret()
ALGORITHM = OIPConfig().auth_algorithm()


@given("an AuthInterceptor protecting the endpoint")
def step_impl(context):
    context.protected_method = METHOD_NAME
    context.interceptor = AuthInterceptor(
        DefaultAdapter(), protected_endpoints={context.protected_method}
    )
    context.servicer, context.handler = (
        AuthTestHelper.create_test_servicer_and_handler()
    )
    context.test_request = AuthTestHelper.create_test_inference_request()


@given("a valid JWT token")
def step_impl(context):
    payload = {"sub": "test-user", "name": "Test User"}
    secret = context.interceptor.config.auth_secret()
    algo = context.interceptor.config.auth_algorithm()
    context.jwt = jwt.encode(payload, secret, algorithm=algo)


@given("an invalid JWT token")
def step_impl(context):
    context.jwt = "invalid.token.value"


@when("a request is made to the protected endpoint")
def step_impl(context):
    if hasattr(context, "jwt"):
        metadata = [("authorization", f"Bearer {context.jwt}")]
    else:
        metadata = []
    mock_context = AuthTestHelper.create_mock_grpc_context(metadata)

    # Create intercepted method
    intercepted_model_infer = AuthTestHelper.create_intercepted_servicer_method(
        context.servicer, context.interceptor, "ModelInfer"
    )

    # Execute the intercepted call
    try:
        loop = asyncio.get_event_loop()
        context.response = loop.run_until_complete(
            intercepted_model_infer(context.test_request, mock_context)
        )
        context.auth_success = True
        context.mock_context = mock_context
    except Exception as e:
        context.error = str(e)
        context.auth_success = False
        context.mock_context = mock_context


@then("the response is successful")
def step_impl(context):
    nt.ok_(context.auth_success, "Expected successful authorization")

    # Check that we got a valid response
    nt.ok_(
        hasattr(context, "response") and context.response is not None,
        "Expected a valid response from the servicer",
    )

    # Verify the request data was passed correctly
    nt.assert_equal(
        context.test_request.model_name,
        context.handler.model_name,
        "Model name should match the request",
    )


@then("the response is UNAUTHENTICATED")
def step_impl(context):
    nt.ok_(
        context.mock_context.abort.called, "Expected abort to be called but it wasn't"
    )
    call_args = context.mock_context.abort.call_args
    args, kwargs = call_args
    nt.ok_(
        args[0] == grpc.StatusCode.UNAUTHENTICATED,
        f"Expected UNAUTHENTICATED status but got {args[0]}",
    )
