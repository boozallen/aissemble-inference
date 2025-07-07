from behave import given, then, when
from aissemble_open_inference_protocol_shared.auth.xacml3_builder import (
    XacmlRequestBuilder,
)
import json


@given("I have a user with a role")
def I_have_a_user_with_a_role(context):
    context.xacml_request_builder = XacmlRequestBuilder()


@when("I build a XACML 3.0 request")
def I_build_a_xacml_3_request(context):
    request = context.xacml_request_builder.build_request(
        user="tom", role="admin", resource="resource1", action="action1"
    )
    context.generated_xacml = json.loads(request)


@then("the request is properly constructed")
def the_request_is_properly_constructed(context):
    # compare context.xacml_request with file
    with open("tests/resources/validation/admin_role_xacml_3_request.json", "r") as f:
        validation_xacml = json.load(f)

    assert context.generated_xacml == validation_xacml, (
        "Generate XACML request did not pass validation"
    )
