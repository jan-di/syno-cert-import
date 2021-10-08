FROM python:3.10.0-alpine3.14

WORKDIR /app

COPY Pipfile* /app/
RUN set -eux; \
    pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy --clear && \
    pip uninstall pipenv -y

ENV PYTHONUNBUFFERED=1
    
COPY . /app/

ENTRYPOINT [ "python", "-u", "/app/deploy.py" ]