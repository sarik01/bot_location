FROM python:3.10.13

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN pip install --upgrade pip


COPY requirements.txt /temp/requirements.txt
COPY . /aiogram3
WORKDIR /aiogram3

RUN pip install -r /temp/requirements.txt

RUN pip install typing-extensions --upgrade

RUN adduser --disabled-password service-user

RUN chown -R service-user:service-user /aiogram3 && chmod 755 /aiogram3

USER service-user