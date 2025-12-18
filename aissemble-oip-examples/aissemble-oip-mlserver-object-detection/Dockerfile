FROM python:3.12-slim

# install uv 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app # set working direcotry

# copy dependency files
COPY pyproject.toml uv.lock ./

# install deps
RUN uv sync --frozen --no-dev

# copy application code
COPY src/object_detection/model.py .
COPY src/object_detection/server.py .

# expose ports
EXPOSE 8080 8081 8082

# run server
CMD ["uv", "run", "python", "src/object_detection/server.py"]