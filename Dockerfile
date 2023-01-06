FROM python:3.11-bullseye as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml /tmp/
COPY ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-bullseye

SHELL [ "/bin/bash", "-ec" ]

COPY --from=requirements-stage /tmp/requirements.txt /setupdir/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade -r /setupdir/requirements.txt
