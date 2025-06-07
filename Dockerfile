# syntax=docker/dockerfile:1

ARG NODE_VERSION=18
ARG PYTHON_VERSION=3.13
ARG BUILD_GROUPS=""

# Build container
FROM node:${NODE_VERSION} AS build

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build


# Runtime container
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_MANAGED_PYTHON=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13 \
    UV_PROJECT_ENVIRONMENT=/venv \
    UV_CACHE_DIR=/app/.cache/uv \
    UV_FROZEN=1 \
    UV_REQUIRE_HASHES=1 \
    UV_VERIFY_HASHED=1


WORKDIR /app

RUN <<EOF
groupadd --system app
useradd --system --home-dir /app --gid app --no-user-group app
EOF

RUN <<EOF
apt-get update --quiet --assume-yes
apt-get install --quiet --assume-yes \
    --option APT::Install-Recommends=false \
    --option APT::Install-Suggests=false \
    curl \
    postgresql-client
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOF

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
COPY --from=build /app/static/assets/ ./static/assets/

RUN python manage.py collectstatic --clear --noinput

RUN chown -R app:app /app/
USER app

EXPOSE 8000

CMD ["bin/app", "web"]
