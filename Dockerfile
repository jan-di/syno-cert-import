FROM python:3.8-alpine3.12

WORKDIR /app

COPY Pipfile* /app/
RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy --clear && \
    pip uninstall pipenv -y
    
COPY . /app/

ENTRYPOINT [ "python", "/app/deploy.py" ]