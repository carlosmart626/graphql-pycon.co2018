#Base image
FROM python:3.6

ENV PYTHONUNBUFFERED=1
ENV CODE=/code

COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR $CODE
