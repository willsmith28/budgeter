FROM python:3.12-slim-bookworm as build-image

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -yqq \
    build-essential \
    libpq-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
COPY ./requirements /app/requirements
RUN pip install -r /app/requirements/dev-requirements.txt


FROM python:3.12-slim-bookworm as final-image
COPY --from=build-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN useradd budgeter


RUN apt-get update && apt-get install --no-install-recommends -yqq \
    libpq-dev \
    netcat-traditional

COPY --chown=budgeter . /app

USER cookbook
ENTRYPOINT [ "/app/entrypoint.sh" ]
