FROM python:3.10.13

WORKDIR /usr/src/times/

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y --force-yes supervisor && \
    apt-get install -y libxslt-dev libxml2-dev screen rsync

# Setup poetry
COPY poetry.lock pyproject.toml ./
RUN pip install "poetry==1.6.1" && \
    poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

COPY . .