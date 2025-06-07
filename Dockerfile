# syntax=docker/dockerfile:1

ARG NODE_VERSION=18
ARG PYTHON_VERSION=3.13
ARG BUILD_GROUPS=""

# Vite assets build container
FROM node:${NODE_VERSION} AS build-vite

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build


# uv build container
FROM python:${PYTHON_VERSION}-slim AS build-uv

ENV DJANGO_SETTINGS_MODULE=explorer.settings \
    DJANGO_ENV=production \
    DEBUG=off \
    PATH="/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_CACHE_DIR=/app/.cache/uv \
    UV_COMPILE_BYTECODE=1 \
    UV_FROZEN=1 \
    UV_LINK_MODE=copy \
    UV_NO_MANAGED_PYTHON=1 \
    UV_PROJECT_ENVIRONMENT=/venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13 \
    UV_REQUIRE_HASHES=1 \
    UV_VERIFY_HASHED=1 \
    VIRTUAL_ENV=/venv

WORKDIR /app

RUN <<EOT
apt-get update --quiet --assume-yes
apt-get install --quiet --assume-yes \
    --option APT::Install-Recommends=false \
    --option APT::Install-Suggests=false \
    curl \
    postgresql-client
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies before copying application code to leverage docker build caching
COPY pyproject.toml uv.lock ./

RUN uv venv ${VIRTUAL_ENV}

RUN --mount=type=cache,target=/app/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    # TODO: Fix the build groups section.
    uv sync --no-dev --no-install-project --no-editable ${BUILD_GROUPS}

# Copy application code (see .dockerignore for excluded files)
COPY . .
COPY --from=build-vite /app/static/assets/ ./static/assets/

RUN python manage.py collectstatic --clear --noinput




### FINAL IMAGE ###

FROM python:${PYTHON_VERSION}-slim AS runtime

ARG PORT=8000
ENV DEBUG=off \
    DJANGO_ENV=production \
    DJANGO_SETTINGS_MODULE=explorer.settings \
    PATH="/venv/bin:$PATH" \
    PORT=${PORT} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/venv

EXPOSE ${PORT}
# ENTRYPOINT ["/bin/bash", "/app/bin/run"]
# CMD ["prod"]

WORKDIR /app

RUN <<EOT
groupadd --system app
useradd --system --home-dir /app --gid app --no-user-group app
EOT

RUN <<EOT
apt-get clean --assume-yes
apt-get update --assume-yes
apt-get install --assume-yes --no-install-recommends \
    bash \
	curl \
    postgresql-client \
apt-get autoremove --assume-yes
apt-get clean --assume-yes
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT

# Copy selectively from builder to optimize final image.
# --link enables better layer caching when base image changes
COPY --link --from=build-uv /venv /venv
COPY --link --from=build-uv /app/explorer /app/explorer
COPY --link --from=build-uv /app/static /app/static
COPY --link --from=build-uv /app/manage.py /app/manage.py

RUN chown -R app:app /app/
USER app
