###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::gRPC with Auth
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import jwt
from datetime import datetime, timedelta, UTC

# These should match the configuration in oip.properties
AUTH_SECRET = "your-secret-key"
AUTH_ALGORITHM = "HS256"


def create_jwt_token(
    username: str, roles: list = None, expires_delta: timedelta = timedelta(hours=1)
) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(UTC) + expires_delta,
        "iat": datetime.now(UTC),
        "roles": roles,
    }

    return jwt.encode(payload, AUTH_SECRET, algorithm=AUTH_ALGORITHM)


def generate_jwt_tokens():
    admin_token = create_jwt_token("admin_user", ["admin"])
    print(f"Admin token (full access): {admin_token}\n")

    user_token = create_jwt_token("regular_user", ["user"])
    print(f"User token (no access to ModelInfer): {user_token}\n")

    print("Use these tokens in your gRPC client metadata:")
    print("metadata = [('authorization', 'Bearer <YOUR_JWT_TOKEN_HERE>')]")
