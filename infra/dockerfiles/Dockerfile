FROM python:3.10-alpine

WORKDIR /app
RUN apk add --no-cache gcc libpq-dev libc-dev python3-dev g++

COPY . /app
COPY ./infra/libs /app/infra/libs
COPY ./infra/envs /app/infra/envs

RUN python -m venv /app/venv

RUN /app/venv/bin/python -m pip install -r /app/infra/libs/requirements.txt

EXPOSE 5200

ENTRYPOINT ["/app/venv/bin/python", "./app/run.py"]
