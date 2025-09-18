import os
import sys


def after_scenario(context, scenario):
    # Clean up test environment variables
    test_env_vars = [
        "KSERVE_GRPC_PORT",
        "KSERVE_WORKERS",
        "FASTAPI_PORT",
        "GRPC_HOST",
        "AUTH_ALGORITHM",
        "OIP_PDP_URL",
        "KSERVE_HTTP_PORT",
    ]

    for var in test_env_vars:
        os.environ.pop(var, None)

    # Restore the original sys.argv if it was saved
    if hasattr(context, "original_argv"):
        sys.argv = context.original_argv
