FROM python:3.11-slim as base

WORKDIR /code

RUN apt update
RUN apt install -y gcc libpq-dev


FROM base as builder

COPY ./poetry.lock  ./pyproject.toml ./
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt


FROM base as final

COPY --from=builder /code/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
