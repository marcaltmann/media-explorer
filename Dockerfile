# syntax=docker/dockerfile:1

ARG NODE_VERSION=24
ARG PYTHON_VERSION=3.14
ARG BUILD_GROUPS=""
ARG DJANGO_ENV=production

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

ARG DJANGO_ENV

ENV DJANGO_SETTINGS_MODULE=explorer.settings \
    DJANGO_ENV=${DJANGO_ENV} \
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
    UV_PYTHON=python3.14 \
    UV_REQUIRE_HASHES=1 \
    UV_VERIFY_HASHED=1 \
    VIRTUAL_ENV=/venv

WORKDIR /app

RUN apt-get update -y && apt-get install -y gettext postgresql-client

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
COPY --from=build-vite /app/vite_assets_dist/ ./vite_assets_dist

RUN python manage.py collectstatic --clear --noinput && python manage.py compilemessages


### FINAL IMAGE ###

FROM python:${PYTHON_VERSION}-slim AS runtime

ARG PORT=8000
ARG DJANGO_ENV

ENV DEBUG=off \
    DJANGO_ENV=${DJANGO_ENV} \
    DJANGO_SETTINGS_MODULE=explorer.settings \
    PATH="/venv/bin:$PATH" \
    PORT=${PORT} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/venv

RUN apt-get update && apt-get install -y curl postgresql-client

WORKDIR /app

RUN groupadd --system app && useradd --system --home-dir /app --gid app --no-user-group app


# Copy selectively from builder to optimize final image.
# --link enables better layer caching when base image changes
COPY --link --from=build-uv /venv /venv
COPY --link --from=build-uv /app/explorer /app/explorer
COPY --link --from=build-uv /app/static /app/static
COPY --link --from=build-uv /app/locale /app/locale
COPY --link --from=build-uv /app/manage.py /app/manage.py
COPY --link --from=build-uv /app/bin /app/bin
COPY --link --from=build-uv /app/config /app/config

RUN chown -R app:app /app/
USER app

# EXPOSE ${PORT}
CMD ["bin/app", "web"]
