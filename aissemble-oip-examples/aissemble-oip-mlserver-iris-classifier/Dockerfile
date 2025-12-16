###
# #%L
# aiSSEMBLE::Open Inference Protocol::Examples::MLServer Iris Classifier
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

FROM ghcr.io/astral-sh/uv:0.9.10-python3.11-bookworm-slim

ARG APP_USERNAME=appuser
ARG USER_UID=10001
ARG USER_GID=$USER_UID

RUN true \
    # Create a non-root user for the app
    && addgroup --system --gid ${USER_GID} ${APP_USERNAME} \
    && adduser --system --uid ${USER_UID} --gid ${USER_GID} --home /home/${APP_USERNAME} ${APP_USERNAME}

# If you need to install something into the container via apt-get
# do so after the "upgrade" command and before the cleanup section
# in the run command below.
RUN true \
    # Update system packages to pull in any security updates.
    && apt-get update \
    && apt-get upgrade -y \
    # Clean up package lists now that we've upgraded.
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/lists/*

# Install the project into `/app`
WORKDIR /app
RUN chown -R ${APP_USERNAME}:${APP_USERNAME} /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --python 3.11

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY --chown=${APP_USERNAME}:${APP_USERNAME} . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --python 3.11

# Change ownership of venv to appuser so it can run as non-root
RUN chown -R ${APP_USERNAME}:${APP_USERNAME} /app/.venv

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# MLServer exposes HTTP on 8080 and gRPC on 8081
EXPOSE 8080
EXPOSE 8081

# Run the MLServer application
CMD ["python", "-m", "iris_classifier.server"]

USER ${APP_USERNAME}

