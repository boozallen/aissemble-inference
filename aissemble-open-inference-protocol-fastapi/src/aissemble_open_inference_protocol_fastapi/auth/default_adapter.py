###
# #%L
# aiSSEMBLE::Open Inference Protocol::FastAPI
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from .authz_adapter_base import AuthzAdapterBase


class DefaultAdapter(AuthzAdapterBase):
    def __init__(self):
        # This is just an example property that is not actually used.
        # A full implementation will make use of a service url.
        self.service_url = "http://localhost:<some port>/<some path>"

    def authorize(self, user: dict, action: str, resource: str) -> bool:
        self.log_authorize(user, action, resource)

        return True
