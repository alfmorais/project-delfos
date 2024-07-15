FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /src
COPY . .

RUN apt-get update -y

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

RUN chmod 777 ./scripts/entrypoint.sh

EXPOSE 8000