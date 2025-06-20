# #%L
# aiSSEMBLE::Extensions::Transform::Spark::Python
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###

import jwt
from datetime import datetime, timedelta
from aissemble_open_inference_protocol_fastapi.config.oip_config import OIPConfig
import os

os.environ["KRAUSENING_BASE"] = "tests/resources/krausening/base"
config = OIPConfig()
SECRET_KEY = config.auth_secret()
ALGORITHM = config.auth_algorithm()


def before_all(context):
    to_encode = {"sub": "some-user-id", "name": "Some User"}
    expires_delta = timedelta(hours=1)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    context.jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
