# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.10.6-slim-bullseye AS python-base

# Port used by this container to serve HTTP.
EXPOSE 4000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ARG BLOGSLEY_ENV

ENV BLOGSLEY_ENV=${BLOGSLEY_ENV} \
  PORT=4000 \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.14 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.local/bin"
  
FROM python-base as blogsley-base

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
  curl \
  wget \
  gnupg \
  build-essential \
  libpq-dev \
  libjpeg62-turbo-dev \
  zlib1g-dev \
  libwebp-dev \
  postgresql-client \
  ca-certificates \
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /blogsley && useradd -d /blogsley -u 1000 blogsley && chown -R blogsley /blogsley

COPY --chown=blogsley:blogsley ./poetry.lock ./pyproject.toml /tmp/
WORKDIR /tmp

# Project initialization:
RUN echo "$BLOGSLEY_ENV" && poetry version \
  && poetry install \
    $(if [ "$BLOGSLEY_ENV" = 'production' ]; then echo '--no-dev'; fi) \
    --no-interaction --no-ansi \
  # Upgrading pip, it is insecure, remove after `pip@21.1`
  && poetry run pip install -U pip \
  # Cleaning poetry installation's cache for production:
  && if [ "$BLOGSLEY_ENV" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi

USER blogsley

FROM blogsley-base AS development

WORKDIR /app
ENTRYPOINT ["bash", "./docker-entrypoint.sh"]
CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--port=4000", "--factory", "blogsley.application:create_app"]
#CMD ["python -m blogsley dev"]

FROM blogsley-base AS production

WORKDIR /app
ENTRYPOINT ["bash", "./docker-entrypoint.sh"]
CMD [ "gunicorn", "--worker-class uvicorn.workers.UvicornWorker", "--config ./gunicorn.conf.py", "blogsley.application:create_app"]
#CMD ["python -m blogsley dev"]
