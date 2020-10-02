FROM python:3.8

RUN apt update
RUN apt install -y libgl1-mesa-glx

RUN pip install poetry
RUN poetry config virtualenvs.create false
WORKDIR /app

COPY poetry.lock /app
COPY pyproject.toml /app

RUN poetry install --no-interaction

COPY . /app
