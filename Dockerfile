FROM docker.io/library/python:3.11.2-bullseye AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

FROM base AS python-deps

COPY Pipfile Pipfile.lock  ./
RUN set -eux; \
    pip install --no-cache-dir pipenv; \
    CI=1 PIPENV_VENV_IN_PROJECT=1 PIP_ONLY_BINARY=:all: pipenv install --deploy --clear

FROM base

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app
COPY . .

CMD [ "python3", "/app/main.py" ]