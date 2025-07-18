###
# #%L
# aiSSEMBLE::Open Inference Protocol Examples::FastAPI with Auth
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import jwt
from datetime import datetime, timedelta

SECRET_KEY = ""  # use a secure key!
ALGORITHM = "HS256"


def create_simple_jwt_token(data: dict, expires_delta: timedelta = timedelta(hours=10)):
    # data["roles"] = "admin"
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
