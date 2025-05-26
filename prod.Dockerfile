FROM ghcr.io/astral-sh/uv:0.6.7-python3.13-bookworm-slim@sha256:5ee2f527d9414c47e7eed6593b68ee959e1789e3ba87e0277627b9999996b1d1 AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY /app/ /app/
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same, e.g., using `python:3.13-slim-bookworm`
# will fail.
FROM python:3.13-slim-bookworm@sha256:8f3aba466a471c0ab903dbd7cb979abd4bda370b04789d25440cc90372b50e04

# Create user and group 'app'
RUN groupadd -r app && useradd -r -g app app

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

# app should run as user app, not root for better security
USER app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

CMD ["gunicorn", "application.main:create_app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--log-level", "critical"]
