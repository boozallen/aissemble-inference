###
# #%L
# aiSSEMBLE::Open Inference Protocol::FastAPI
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from abc import ABC, abstractmethod
from krausening.logging import LogManager
import json
from typing import Optional


class AuthAdapterBase(ABC):
    """
    Check if the user is allowed to perform the action on the resource
    """

    logger = LogManager.get_instance().get_logger("AuthzAdapterBase")

    @abstractmethod
    def _authorize_impl(
        self, user: dict, resource: str, action: str, role: Optional[str] = None
    ) -> bool:
        pass

    def authorize(
        self, user: dict, resource: str, action: str, role: Optional[str] = None
    ) -> bool:
        self.log_authorize(user=user, resource=resource, action=action, role=role)

        return self._authorize_impl(
            user=user, resource=resource, action=action, role=role
        )

    def log_authorize(
        self, user: dict, resource: str, action: str, role: Optional[str] = None
    ):
        user_for_logging = json.dumps(user, indent=2)

        self.logger.info("Authorization start")
        self.logger.info(f"User:\n{user_for_logging}")
        self.logger.info(f"action: {action}")
        self.logger.info(f"resource: {resource}")
        if role:
            self.logger.info(f"role: {role}")
