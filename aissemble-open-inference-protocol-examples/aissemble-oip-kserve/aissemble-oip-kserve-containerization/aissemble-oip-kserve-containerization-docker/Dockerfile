#HABUSHU_BUILDER_STAGE - HABUSHU GENERATED CODE (DO NOT MODIFY)
FROM docker.io/python:3.12 AS habushu_builder

# Install pipx
RUN python -m ensurepip --upgrade
RUN python -m pip install --user pipx

# Poetry and supporting plugin installations
RUN $HOME/.local/bin/pipx install poetry==2.0.1 && \
    $HOME/.local/bin/poetry self add poetry-plugin-bundle@1.5.0

WORKDIR /work-dir
COPY --chown=1001 /target/containerize-support ./containerize-support/
RUN find . -type f -name pyproject.toml -exec sed -i 's|develop[[:blank:]]*=[[:blank:]]*true|develop = false|g' {} \;

USER root
WORKDIR /work-dir/containerize-support/aissemble-open-inference-protocol-examples/aissemble-oip-kserve/aissemble-oip-kserve-inference
ENV POETRY_CACHE_DIR="/.cache/pypoetry"

# Export target project's virtual environment to /opt/venv
RUN --mount=type=cache,target=${POETRY_CACHE_DIR} \
    $HOME/.local/bin/poetry lock && \
    $HOME/.local/bin/poetry bundle venv /opt/venv
#HABUSHU_BUILDER_STAGE - HABUSHU GENERATED CODE (END)

#HABUSHU_FINAL_STAGE - HABUSHU GENERATED CODE (DO NOT MODIFY)
FROM docker.io/python:3.12-slim AS final

# Copy venv from builder and activate by adding to the path
COPY --from=habushu_builder --chown=1001 --chmod=744 /opt/venv /opt/venv/
ENV PATH="/opt/venv/bin:$PATH"
#HABUSHU_FINAL_STAGE - HABUSHU GENERATED CODE (END)

# Copy the krausening properties from the builder stage
COPY --from=habushu_builder /work-dir/containerize-support/aissemble-open-inference-protocol-examples/aissemble-oip-kserve/aissemble-oip-kserve-inference/src/resources /opt/app/resources

# Set KRAUSENING_BASE to point to the copied properties
ENV KRAUSENING_BASE="/opt/app/resources/krausening/base"

COPY resources/model /model

ENTRYPOINT ["/opt/venv/bin/python3.12", "-m", "aissemble_oip_kserve_inference.main"]
