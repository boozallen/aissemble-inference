FROM redhat/ubi9:latest  AS builder
# Install gcc and python3-dev in order to build any packages that aren't published as wheels for aarch64 support
RUN dnf upgrade -y && dnf install -y python3.11 python3.11-devel python3.11-pip gcc
# Install Poetry and the poetry-plugin-bundle via pip, using a separate virtual environment for Poetry as
# recommended by official Poetry documentation
WORKDIR /opt
ENV POETRY_HOME=/opt/poetry
RUN python3.11 -m venv $POETRY_HOME && $POETRY_HOME/bin/pip install poetry poetry-plugin-bundle
ENV PATH="$POETRY_HOME/bin:${PATH}"

WORKDIR /app

COPY . .

ENV POETRY_CACHE_DIR="$POETRY_HOME/.cache/"
RUN --mount=type=cache,target=/opt/poetry/.cache \
  sed -i 's|develop[[:blank:]]*=[[:blank:]]*true|develop = false|g' pyproject.toml && \
  poetry lock && \
  poetry bundle venv --only=main /venv

# Install Python 3.11 on a slimmed down ubi9-minimal image, copy the pre-built venv, and use it
# to execute the inference service
FROM redhat/ubi9-minimal:latest
RUN microdnf install -y python3.11

COPY --from=builder /venv /venv

COPY /model /model

ENTRYPOINT ["/venv/bin/python3.11", "-m", "aissemble-oip-kserve-inference.main"]