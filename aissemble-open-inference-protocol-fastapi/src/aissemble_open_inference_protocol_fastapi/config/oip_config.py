###
# #%L
# aiSSEMBLE::Open Inference Protocol::FastAPI
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import os
from krausening.properties import PropertyManager


class OIPConfig:
    """
    Configurations for embedding, read from the embeddings properties file.
    """

    DEFAULT_ALGORITHM = "HS256"

    def __init__(self):
        self.properties = PropertyManager.get_instance().get_properties(
            "oip.properties"
        )

    def auth_secret(self):
        """
        Returns the auth secret key
        """
        value = self.properties.getProperty("auth_secret", "")
        environ_override = os.getenv("AUTH_SECRET")
        return environ_override if environ_override else value

    def auth_algorithm(self):
        """
        Returns the auth algorithm
        """
        value = self.properties.getProperty("auth_algorithm", self.DEFAULT_ALGORITHM)
        environ_override = os.getenv("AUTH_ALGORITHM")
        return environ_override if environ_override else value
