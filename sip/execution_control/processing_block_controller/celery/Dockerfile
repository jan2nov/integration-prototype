FROM python:3.6.4-alpine3.7
LABEL maintainer="Benjamin Mort <ben.mort@gmail.com>"

RUN pip install --no-cache-dir -U "celery[redis]"

WORKDIR /app
COPY app/*.py app/

ENTRYPOINT ["celery", "-A", "app.tasks", "worker", "--loglevel=info"]
