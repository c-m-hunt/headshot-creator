FROM python:3.12

RUN apt update
RUN apt install -y libgl1-mesa-glx libhdf5-dev

RUN pip install uv
WORKDIR /app

COPY uv.lock /app
COPY pyproject.toml /app
RUN uv sync --no-interaction
COPY . /app
