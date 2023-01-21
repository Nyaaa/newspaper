FROM python:3.11-alpine
RUN mkdir /app
WORKDIR /app
RUN pip install poetry && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml .env /app/
RUN poetry install -n --no-root --only main --no-cache

COPY ./newspaper ./