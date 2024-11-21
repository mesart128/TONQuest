FROM python:3.11.7

WORKDIR /usr/src/ton_quests/


ENV POETRY_VERSION=1.6.1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

#ADD id_ed25519 /root/.ssh/id_ed25519

RUN apt-get update -y && \
    apt-get install -y --force-yes supervisor && \
    apt-get install -y libxslt-dev libxml2-dev screen rsync

COPY poetry.lock pyproject.toml ./

RUN pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

ADD /deploy/node_server/gunicorn.conf  /etc/supervisor/conf.d/background.conf

COPY . .
