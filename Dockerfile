FROM python:3.9-alpine


COPY ./requirements.txt /requirements.txt
COPY . /hackeryesno
WORKDIR /hackeryesno

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user

