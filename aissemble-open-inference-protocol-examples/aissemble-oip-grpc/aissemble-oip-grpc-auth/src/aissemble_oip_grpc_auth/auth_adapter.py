###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::gRPC with Auth
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from aissemble_open_inference_protocol_shared.auth.auth_adapter_base import (
    AuthAdapterBase,
)
from typing import Optional


class AuthAdapter(AuthAdapterBase):
    """
    A simple Authorization adapter that demonstrates basic role-based access control.

    This example shows how to implement custom authorization logic:
    - 'admin' role: Can access all endpoints
    - 'user' role: Can access only ServerReady
    - No role or unknown role: Denied access
    """

    def __init__(self):
        super().__init__()

        # Define which endpoints each role can access
        self.role_permissions = {
            "admin": {
                # Admins can access everything
                "/inference.GrpcInferenceService/ModelInfer",
                "/inference.GrpcInferenceService/ModelMetadata",
                "/inference.GrpcInferenceService/ModelReady",
                "/inference.GrpcInferenceService/ServerReady",
            },
            "user": {
                # Regular users can access only ServerReady
                "/inference.GrpcInferenceService/ServerReady",
            },
        }

    def _authorize_impl(
        self,
        user: dict,
        resource: str,
        action: str,
        request_url: str,
        role: Optional[str] = None,
    ) -> bool:
        # Extract user information for logging
        username = user if isinstance(user, str) else user.get("sub", "unknown")

        # Get roles from the JWT token
        user_roles = []
        if role:
            if isinstance(role, str):
                user_roles = [role]
            elif isinstance(role, list):
                user_roles = role

        self.logger.info(
            f"Checking authorization for user '{username}' with roles {user_roles} for endpoint '{request_url}'"
        )

        # If no roles, deny access
        if not user_roles:
            self.logger.info(f"Access denied for user '{username}': No roles found")
            decision = False
        else:
            # Check endpoint-specific permissions
            decision = self.check_endpoint_access(user_roles, request_url)

            if decision:
                self.logger.info(
                    f"Access granted for user '{username}' with role(s) {user_roles} for endpoint '{request_url}'"
                )
            else:
                self.logger.info(
                    f"Access denied for user '{username}': No valid roles for endpoint '{request_url}'"
                )
        return decision

    def check_endpoint_access(self, user_roles: list, endpoint: str) -> bool:
        """
        Check if any of the user's roles can access a specific endpoint.
        """
        for role in user_roles:
            if role in self.role_permissions:
                if endpoint in self.role_permissions[role]:
                    return True
        return False
