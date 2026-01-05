# Use a Python base image
FROM python:3.13-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir -p /app

ENV APP_HOME=/app

WORKDIR $APP_HOME

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy only the dependency files first
COPY pyproject.toml uv.lock $APP_HOME

# Copy files
COPY . $APP_HOME

ENV UV_PROJECT_ENVIRONMENT="/usr/local"

# Install the project
RUN uv sync --frozen

# Expose port
EXPOSE 8000

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Default command (can be overridden in docker-compose)
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
