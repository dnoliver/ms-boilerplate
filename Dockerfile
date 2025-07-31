FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye AS dev

RUN pip install poetry==2.1.3

CMD ["sleep", "infinity"]

FROM python:3.12-bullseye AS builder

RUN pip install poetry==2.1.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock README.md scripts.py ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --with dev --no-root

FROM python:3.12-slim-bullseye AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app ./app

EXPOSE 8000

ENTRYPOINT ["fastapi", "run"]
