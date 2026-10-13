# Build:  docker build -t dsan6700-hw .
# Run:    docker run --env-file .env -p 8000:8000 dsan6700-hw
#
# Configuration is supplied at run time with --env-file; no .env file is
# copied into the image.

# Slim Python base: the service runs on CPU, so no CUDA base image is needed
FROM python:3.12-slim

# curl is used by the HEALTHCHECK below
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (pinned version for reproducibility)
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /usr/local/bin/uv

# Non-root user to run the service
RUN useradd --create-home app

WORKDIR /app

# Install dependencies from the lock file before copying the source, so this
# layer is cached and only rebuilds when pyproject.toml or uv.lock change
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy the source and install the project itself
COPY README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev

USER app

EXPOSE 8000

# Hit the /health endpoint; the start period gives the model time to load
HEALTHCHECK --interval=30s --timeout=5s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["/app/.venv/bin/uvicorn", "mypkg.mypkg:app", "--host", "0.0.0.0", "--port", "8000"]
