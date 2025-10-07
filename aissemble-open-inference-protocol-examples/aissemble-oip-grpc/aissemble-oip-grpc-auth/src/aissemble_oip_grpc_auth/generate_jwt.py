###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::gRPC with Auth
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
