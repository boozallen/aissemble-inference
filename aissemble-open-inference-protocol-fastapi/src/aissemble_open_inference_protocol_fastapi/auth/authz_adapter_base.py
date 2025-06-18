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


class AuthzAdapterBase(ABC):
    """
    Check if the user is allowed to perform the action on the resource
    """

    logger = LogManager.get_instance().get_logger("AuthzAdapterBase")

    @abstractmethod
    def authorize(self, user: dict, action: str, resource: str) -> bool:
        pass

    def log_authorize(self, user: dict, action: str, resource: str):
        user_for_logging = json.dumps(user, indent=2)

        self.logger.info("Authorization start")
        self.logger.info(f"User:\n{user_for_logging}")
        self.logger.info(f"action: {action}")
        self.logger.info(f"resource: {resource}")
